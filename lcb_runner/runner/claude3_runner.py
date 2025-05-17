import os
from time import sleep

try:
    from anthropic import Anthropic
except ImportError as e:
    pass

from lcb_runner.runner.base_runner import BaseRunner
from openai import OpenAI

class Claude3Runner(BaseRunner):
    # client = Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))
    # client = Anthropic(api_key="ak-58d7efgh23i4jkl67mno89pqrs01tuv6k5", base_url= "https://models-proxy.stepfun-inc.com/v1")
    client = OpenAI(api_key="ak-58d7efgh23i4jkl67mno89pqrs01tuv6k5", base_url= "https://models-proxy.stepfun-inc.com/v1")
    def __init__(self, args, model):
        super().__init__(args, model)
        self.client_kwargs: dict[str | str] = {
            "model": args.model,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "top_p": args.top_p,
        }

    def _run_single(self, prompt: tuple[str, str]) -> list[str]:

        def __run_single(counter):
            try:
                # print(prompt)
                messages = [
                    {
                        "role": "system",
                        "content": prompt[0],
                    }
                ]
                messages.extend(prompt[1])
                # import json
                # print(json.dumps(messages, indent=4))
                response = Claude3Runner.client.chat.completions.create(
                    messages=messages,
                    **self.client_kwargs,
                )
                # response = self.client.messages.create(
                #     system=prompt[0],
                #     messages=prompt[1],
                #     **self.client_kwargs,
                # )
                # content = "\n".join([x.text for x in response.content])
                content = response.choices[0].message.content
                # print(content)
                return content
            except Exception as e:
                print("Exception: ", repr(e), "Sleeping for 20 seconds...")
                sleep(20 * (11 - counter))
                counter = counter - 1
                if counter == 0:
                    print(f"Failed to run model for {prompt}!")
                    print("Exception: ", repr(e))
                    raise e
                return __run_single(counter)

        outputs = []
        try:
            for _ in range(self.args.n):
                outputs.append(__run_single(10))
        except Exception as e:
            raise e

        return outputs
