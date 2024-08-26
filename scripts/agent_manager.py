from models import create_chat_completion

next_key = 0
agents = {}  # key: (task, history, model)

def create_agent(task, prompt, model):
    global next_key, agents
    msgs = [{"role": "user", "content": prompt}]
    reply = create_chat_completion(model=model, messages=msgs)
    msgs.append({"role": "assistant", "content": reply})
    key = next_key
    next_key += 1
    agents[key] = (task, msgs, model)
    return key, reply

def message_agent(key, message):
    task, msgs, model = agents[int(key)]
    msgs.append({"role": "user", "content": message})
    reply = create_chat_completion(model=model, messages=msgs)
    msgs.append({"role": "assistant", "content": reply})
    return reply

def list_agents():
    return [(k, t) for k, (t, _, _) in agents.items()]

def delete_agent(key):
    return agents.pop(int(key), None) is not None
