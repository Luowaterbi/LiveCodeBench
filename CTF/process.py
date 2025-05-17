import json
import pickle
import zlib
import base64
from multiprocessing import Pool, cpu_count
from testing_util import run_test, execute_output
from tqdm import tqdm
import os


def get_easy():
    """
    提取所有easy难度的题目
    """
    from datasets import load_dataset
    ds = load_dataset("/data/datasets/code_generation_lite", split="test", version_tag="release_v3", trust_remote_code=True)
    res = []
    print(json.dumps(ds[0], indent=4))
    for d in ds:
        if d["difficulty"] == "easy":
            res.append(d)
    print(len(res))
    json.dump(res, open("easy.json", "w"), indent=4)


def load_private():
    """
    加载easy题目的private test cases
    """
    ds = json.load(open("easy.json"))
    for d in ds:
        d["private_test_cases"] = json.loads(
                pickle.loads(
                    zlib.decompress(
                        base64.b64decode(d["private_test_cases"].encode("utf-8"))  # type: ignore
                    )
                )
            )
    json.dump(ds, open("easy_with_tests.json", "w"), indent=4)


def transfer2ctf():
    """
    将原始题目的信息转移到ctf题目中
    """
    def extract_func_name(code: str) -> str:
        code = code.split("\n")
        for l in code:
            if "def " in l:
                return l.split("def ")[1].split("(")[0]

    ds = json.load(open("easy_with_tests.json"))
    ctf = json.load(open("ctf_problems.json"))
    ori = {i: d for i, d in enumerate(ds)}
    res = []
    for c in ctf:
        if c["starter_code"] != "":
            func_name = extract_func_name(c["starter_code"])
            c["metadata"] = json.dumps({"func_name": func_name})
        else:
            c["metadata"] = ""
        c["idx"] = int(c["idx"])
        o = ori[c["idx"]]
        c["question_title"] = "ctf_" + o["question_title"]
        c["platform"] = "ctf_" + o["platform"]
        c["question_id"] = "ctf_" + o["question_id"]
        c["contest_id"] = "ctf"
        c["contest_date"] = "2025-02-16T00:00:00"
        c["private_test_cases"] = o["private_test_cases"]
        c["difficulty"] = "easy"
        res.append(c)
    json.dump(ctf, open("easy_ctf.json", "w"), indent=4)

# transfer2ctf()

def get_evaluation_sample(d, all=True):
    """
    将test case转换成testing_util.py需要的形式
    """
    if all:
        return {
            "input_output": json.dumps(
                {
                    "inputs": [
                        t["input"]
                        for t in json.loads(d["public_test_cases"]) + d["private_test_cases"]
                    ],
                    "outputs": [
                        t["output"]
                        for t in json.loads(d["public_test_cases"]) + d["private_test_cases"]
                    ],
                    "fn_name": json.loads(d["metadata"]).get("func_name", None) if d["metadata"] else None,
                }
            )
        }
    else:
        return {
            "input_output": json.dumps(
                {
                    "inputs": [t["input"] for t in json.loads(d["public_test_cases"])],
                    "outputs": [t["output"] for t in json.loads(d["public_test_cases"])],
                    "fn_name": json.loads(d["metadata"]).get("func_name", None) if d["metadata"] else None,
                }
            )
        }


def verify_public_testcase(file, save_name):
    """
    先测一下solution能不能通过public test cases
    """
    from concurrent.futures import as_completed, ProcessPoolExecutor
    ds = json.load(open(f"/home/i-luoxianzhen/GAR/CTF/{file}.json"))
    not_down = open(f"{save_name}.jsonl", "a")
    with ProcessPoolExecutor(max_workers=10) as executor:
        pbar = tqdm(total=len(ds))
        futures = {
            executor.submit(run_test, get_evaluation_sample(d, all=False), test=d["solution"], debug=False, timeout=7*len(d["public_test_cases"])+5): d
            for d in ds
        }
        for future in as_completed(futures):
            res, meta = future.result()
            if not all(res):
                print(json.dumps(meta, indent=4))
                futures[future]["meta"] = meta
                # not_down.append(futures[future])
                not_down.write(json.dumps(futures[future]) + "\n")
            pbar.update(1)
    # json.dump(not_down, open("not_down.json", "w"), indent=4)


def jsonl2md(file, save_name):
    """
    将jsonl转换成markdown
    """
    ds = [json.loads(l) for l in open(f"{file}.jsonl").readlines()]
    os.makedirs(save_name, exist_ok=True)
    for d in ds:
        writer = open(f"{save_name}/{d['idx']}.md", "w")
        writer.write("## Question Content\n\n")
        writer.write(f"{d['question_content']}\n\n")
        writer.write("## Solution\n\n")
        writer.write(f"{d['solution']}\n\n")
        writer.write("## Public Test Cases\n\n")
        writer.write(f"{d['public_test_cases']}\n\n")
        writer.write("## Meta\n\n")
        writer.write(f"{json.dumps(d['meta'], indent=4)}\n\n")
        writer.close()


def update_testcases():
    """
    更新test cases
    """
    ds = json.load(open("easy_ctf.json"))
    down = os.listdir("rerun_not_down/down")
    rerun = []
    for d in ds:
        if str(d["idx"]) + ".md" in down:
            try:
                content = open(f"rerun_not_down/down/{d['idx']}.md").read()
            except Exception as e:
                print(d["idx"])
                exit()
            if "## Question Content" in content:
                d["question_content"] = content.split("## Question Content")[1].split("## Solution")[0].strip()
            else:
                d["question_content"] = content.split("## Question:")[1].split("## Solution\n\n")[0].strip()
            d["solution"] = content.split("## Solution\n\n")[1].split("## Public Test Cases\n\n")[0].strip()
            d["public_test_cases"] = content.split("## Public Test Cases\n\n")[1].split("## Meta\n\n")[0]
            rerun.append(d)
    json.dump(rerun, open("rerun_rxl.json", "w"), indent=4)
    verify_public_testcase("rerun_rxl", "rerun_rxl_not_down")
    jsonl2md("rerun_rxl_not_down", "rerun_rxl_not_down")


def why_no_output():
    """
    发现有一些代码到testing util中没有输出，看看什么原因
    """
    files = os.listdir("/home/i-luoxianzhen/GAR/CTF/rerun_not_down/stdin_bug")
    for f in files:
        if not f.endswith(".md"):
            continue
        content = open(f"/home/i-luoxianzhen/GAR/CTF/rerun_not_down/stdin_bug/{f}").read()
        sol = content.split("## Solution\n\n")[1]
        sol, public_testcase = sol.split("## Public Test Cases\n\n")
        sol = sol.strip()
        public_testcase = public_testcase.split("\n\n## Meta\n\n")[0]
        d = {
            "public_test_cases": public_testcase,
            "metadata": ""
        }
        res, meta = run_test(get_evaluation_sample(d, all=False), test=sol, debug=True, timeout=7*len(json.loads(public_testcase))+5)
        if not all(res):
            print(f)
            print(json.dumps(meta, indent=4))


def rerun_replace(lst=["", "_stdin", "_xy"], file="easy_ctf"):
    """
    用rerun后的正确的代替原来的内容
    """
    ds = json.load(open(f"{file}.json"))
    rerun = {}
    for suf in lst:
        rerun_suf = json.load(open(f"rerun{suf}.json"))
        for r in rerun_suf:
            rerun[r["idx"]] = r
    new_ctf = []
    for d in ds:
        if d["idx"] in rerun:
            new_ctf.append(rerun[d["idx"]])
        else:
            new_ctf.append(d)
    json.dump(new_ctf, open(f"easy_ctf2.json", "w"), indent=4)


def get_ctf_testcases(file, bad_save_name, good_save_name):
    """
    执行原始数据的test cases input，获取output
    """
    from concurrent.futures import as_completed, ProcessPoolExecutor
    ds = json.load(open(f"/home/i-luoxianzhen/GAR/CTF/{file}.json"))
    not_down = open(f"{bad_save_name}.jsonl", "a")
    down = open(f"{good_save_name}.jsonl", "a")
    with ProcessPoolExecutor(max_workers=10) as executor:
        pbar = tqdm(total=len(ds))
        futures = {
            executor.submit(execute_output, get_evaluation_sample(d, all=True), test=d["solution"], debug=False, timeout=6): d
            for d in ds
        }
        for future in as_completed(futures):
            res, meta = future.result()
            if not all(res):
                print(json.dumps(meta, indent=4))
                futures[future]["meta"] = meta
                # not_down.append(futures[future])
                not_down.write(json.dumps(futures[future]) + "\n")
            else:
                ori_data = futures[future]
                testtype = "functional" if ori_data["starter_code"] else "stdin"
                ori_data["new_public_test_cases"] = []
                ori_data["private_test_cases"] = []
                    
                for idx, (i, o) in enumerate(zip(meta["inputs"], meta["outputs"])):
                    new_testcase = {"input": i, "output": o, "testtype": testtype}
                    if idx < len(json.loads(ori_data["public_test_cases"])):
                        ori_data["new_public_test_cases"].append(new_testcase)
                    else:
                        ori_data["private_test_cases"].append(new_testcase)
                down.write(json.dumps(ori_data) + "\n")
            pbar.update(1)


def look_bad_ctf():
    """
    查看bad_ctf中的数据
    """
    data = open("bad_ctf.jsonl").readlines()
    os.makedirs("bad_ctf", exist_ok=True)
    for d in data:
        d = json.loads(d)
        writer = open(f"bad_ctf/{d['idx']}.md", "w")
        writer.write("## Meta\n\n")
        writer.write(json.dumps(d["meta"], indent=4) + "\n\n")
        writer.write("## Solution\n\n")
        writer.write("```python\n"+ d["solution"] + "\n```\n\n")
        writer.write("## Question Content\n\n")
        writer.write(d["question_content"] + "\n\n")


def process_good_ctf():
    """
    1. 去除good_ctf.jsonl重复的
    2. 更新xmz, rxl修改后替换good_ctf.jsonl中
    """
    rxl = {d["idx"]:d for d in json.load(open("rerun_rxl.json"))}
    xmz= {d["idx"]:d for d in json.load(open("rerun_xmz.json"))}
    data = open("good_ctf.jsonl").readlines()
    data = reversed(data)
    res = {}
    for d in data:
        d = json.loads(d)
        if d["idx"] in res:
            print('duplicate', d["idx"])
            continue
        if d["idx"] in xmz:
            d["question_content"] = xmz[d["idx"]]["question_content"]
            d["public_test_cases"] = xmz[d["idx"]]["public_test_cases"]
            print(d["idx"], "replace!")
        if d["idx"] in rxl:
            d["question_content"] = rxl[d["idx"]]["question_content"]
            d["public_test_cases"] = rxl[d["idx"]]["public_test_cases"]
            print(d["idx"], "replace!")
        # 人工check一下有没有问题
        # if isinstance(d["new_public_test_cases"][0]["output"], list):
        #     for t in d["new_public_test_cases"]:
        #         t["output"] = " ".join(t["output"]) + "\n"
        # assert d["public_test_cases"].strip() == json.dumps(d["new_public_test_cases"]), (d["idx"], "\n", d["public_test_cases"], json.dumps(d["new_public_test_cases"]))
        del d["new_public_test_cases"]
        d["private_test_cases"] = json.dumps(d["private_test_cases"])
        if d["metadata"] == "":
            d["metadata"] = "{}"
        res[d["idx"]] = d
    values = list(res.values())
    json.dump(values, open("good_ctf.json", "w"), indent=4)


def process_easy():
    """
    得到good_ctf对应的easy problem
    """
    ds = json.load(open("good_ctf.json"))
    idxes = [d["idx"] for d in ds]
    easy = json.load(open("easy.json"))
    res = []
    for i, d in enumerate(easy):
        if i in idxes:
            res.append(d)
    print("easy:", len(res))
    json.dump(res, open("good_easy.json", "w"), indent=4)


def process_output():
    """
    对比结果发现好多expected的是list，导致跟output误判了，需要处理一下
    """
    ds = json.load(open("./good_ctf.json", 'r'))
    real = json.load(open("./easy_with_tests.json", 'r'))
    real = {i: r for i, r in enumerate(real)}
    for d in ds:
        private_test_cases = json.loads(d["private_test_cases"])
        for testcase in private_test_cases:
            try :
                output = eval(testcase["output"])
                if isinstance(output, list) and len(output) == 1:
                    try:
                        ori_output = eval(real[d["idx"]]["private_test_cases"][0]["output"])
                    except Exception as e:
                        ori_output = None
                    if isinstance(ori_output, list):
                        continue
                    output = output[0]
                    testcase["output"] = output
            except Exception as e:
                # print(d["idx"], testcase["output"], e)
                pass
        d["private_test_cases"] = json.dumps(private_test_cases)
    json.dump(ds, open("good_ctf2.json", 'w'), indent=4)

if __name__ == "__main__":
    # verify_public_testcase()
    # jsonl2md()
    # update_testcases()
    # why_no_output()
    # rerun_replace()
    # get_ctf_testcases("easy_ctf2", "bad_ctf", "good_ctf")
    # clean_repeate()

    # rerun_xmz还没有合并

    # look_bad_ctf()
    # process_good_ctf()
    process_output()