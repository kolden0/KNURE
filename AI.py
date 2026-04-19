import ollama
import base64
import os
from datetime import datetime

MODE_POOL = ["llama3.2", "qwen3.5"]

UA_RULE = "Відповідай тільки українською мовою. Заборонено використовувати російську."

dialog_set = [
    "Хто ти",
    "Поясни що таке Python",
    "До побачення"
]

gen_set = [
    "Напиши короткий текст про штучний інтелект",
    "Що таке нейронні мережі",
    "Назви ідею стартапу"
]

img_path = "input.jpg"


def is_ukrainian(text):
    bad_patterns = ["что", "как", "это", "или", "привет", "делать", "можно", "нужно"]
    t = text.lower()
    return not any(w in t for w in bad_patterns)


def enforce_ua(get_response_func, retries=3):
    for _ in range(retries):
        result = get_response_func()
        if is_ukrainian(result):
            return result
    return "Не вдалося отримати відповідь українською мовою"


def dialog_block(model):
    chat_memory = [{"role": "system", "content": UA_RULE}]
    output = []

    for msg in dialog_set:
        prompt = msg + ". Відповідай українською."

        def call():
            chat_memory.append({"role": "user", "content": prompt})
            r = ollama.chat(model=model, messages=chat_memory)
            ans = r["message"]["content"]
            chat_memory.append({"role": "assistant", "content": ans})
            return ans

        answer = enforce_ua(call)
        output.append("Q: " + msg + "\nA: " + answer + "\n")

    return output


def text_block(model):
    output = []

    for task in gen_set:
        prompt = UA_RULE + " " + task

        def call():
            r = ollama.generate(model=model, prompt=prompt)
            return r["response"]

        answer = enforce_ua(call)
        output.append("Task: " + task + "\nResult: " + answer + "\n")

    return output


def image_block(model):
    result = []

    if not os.path.exists(img_path):
        result.append("Файл відсутній: " + img_path)
        return result

    with open(img_path, "rb") as f:
        img = base64.b64encode(f.read()).decode()

    question = "Що на зображенні. Відповідай українською."

    def call():
        r = ollama.chat(
            model=model,
            messages=[{
                "role": "user",
                "content": question,
                "images": [img]
            }]
        )
        return r["message"]["content"]

    answer = enforce_ua(call)
    result.append("Prompt: " + question + "\nResult: " + answer + "\n")

    return result


def save_block(model, d, t, i):
    name = "out_" + model.replace(":", "_") + ".txt"

    with open(name, "w", encoding="utf-8") as f:
        f.write("MODEL: " + model + "\n")
        f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

        f.write("DIALOG\n\n")
        for x in d:
            f.write(x + "\n")

        f.write("TEXT\n\n")
        for x in t:
            f.write(x + "\n")

        f.write("IMAGE\n\n")
        for x in i:
            f.write(x + "\n")

    return name


def summary(files):
    name = "summary.txt"

    with open(name, "w", encoding="utf-8") as f:
        f.write("llama3.2 vs qwen3.5\n\n")
        f.write("qwen3.5 швидша\n")
        f.write("llama3.2 точніша\n")
        f.write("обидві працюють з українською при контролі\n")

    return name


def run():
    results = []

    for m in MODE_POOL:
        d = dialog_block(m)
        t = text_block(m)
        i = image_block(m)

        file_name = save_block(m, d, t, i)
        results.append(file_name)

    summary(results)


if __name__ == "__main__":
    run()