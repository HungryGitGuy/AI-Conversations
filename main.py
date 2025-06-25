import ollama, json #json is only used to write the conversation to a file

print("")

sessionSelectionStatus = input("sessions are text files that let you reuse system messages and a beginning message. \nWether or not you use a session, a log file will still be created. \n\nenter an existing session name to load an old one, enter a new one to create a new one, or enter nothing to not use a session at all.\nyour input: ")

if sessionSelectionStatus == "":
    print("Sessions not being used.")
    modelsSelected = False
    while not modelsSelected:
        model1Name = input("Model 1's name (if none is specified, it will be dolphin-llama3): ")
        model2Name = input("Model 1's name (if none is specified, it will be gemma3): ")
        try:
            ollama.show(model1Name)
        except

    model1Name = model1Name if model1Name != "" else "dolphin-llama3"
    model2Name = model2Name if model2Name != "" else "gemma3"

    autoMode = input("Automatic mode will make the program not ask you for anything or pause the conversation and will simply run until stopped forcibly. \nDo you want automatic mode? (y/n)")

    defaultSystemMessage = "You are an autonomous AI agent who can read text and respond with text."

    customSystemMessage1 = input(f"system message for {model1Name} (if no system message is specified then a default one will be used): ")
    customSystemMessage2 = input(f"system message for {model2Name} (if no system message is specified then a default one will be used): ")

    system1 = customSystemMessage1 if customSystemMessage1 != "" else defaultSystemMessage
    system2 = customSystemMessage2 if customSystemMessage2 != "" else defaultSystemMessage

    messages1 = [
        {"role": "system", "content": system1}
    ]

    messages2 = [
        {"role": "system", "content": system2}
    ]

    first_message = input("What's the message that will start the conversation? AI 1 will think this is something they said, and AI 2 will see this as the first prompt. \n")

    messages1.append({"role": "assistant", "content": first_message})
    messages2.append({"role": "user", "content": first_message})

else:
    try:
        with open(f"sessions/{sessionSelectionStatus}.txt", "r") as sessionfile:
            model1Name = sessionfile.readline()[0:-1]
            print(f"model1Name = {model1Name}")
            model2Name = sessionfile.readline()[0:-1]
            print(f"model2Name = {model2Name}")
            system1 = sessionfile.readline()[0:-1]
            print(f"system1 = {system1}")
            system2 = sessionfile.readline()[0:-1]
            print(f"system2 = {system2}")
            autoMode = sessionfile.readline()[0:-1]
            print(f"autoMode = {autoMode}")
            first_message = sessionfile.readline()[0:-1]
            print(f"first_message = {first_message}")

            print("\nLoading file finished! \n")
        messages1 = [
            {"role": "system", "content": system1}, 
            {"role": "assistant", "content": first_message}
        ]
        
        messages2 = [
            {"role": "system", "content": system2}, 
            {"role": "user", "content": first_message}
        ]
        
    except Exception as e: # TODO: find out what the error is and explicitly catch it so any other errors can be found normally
        print(f"Session file does not exist and will be created in ./sessions/ as {sessionSelectionStatus}.txt")

        model1Name = input("Model 1's name (if none is specified, it will be dolphin-llama3): ")
        model2Name = input("Model 2's name (if none is specified, it will be gemma3): ")
        model1Name = model1_name if model1Name != "" else "dolphin-llama3"
        model2Name = model2_name if model2Name != "" else "gemma3"    
        
        defaultSystemMessage = "You are an autonomous AI agent who can read text and respond with text."
        
        customSystemMessage1 = input(f"system message for {model1_name} (if no system message is specified then a default one will be used): ")
        customSystemMessage2 = input(f"system message for {model2_name} (if no system message is specified then a default one will be used): ")
        
        system1 = customSystemMessage1 if customSystemMessage1 != "" else defaultSystemMessage
        system2 = customSystemMessage2 if customSystemMessage2 != "" else defaultSystemMessage

        messages1 = [
            {"role": "system", "content": system1}
        ]
        
        messages2 = [
            {"role": "system", "content": system2}
        ]
        
        first_message = input("What's the message that will start the conversation? AI 1 will think this is something they said, and AI 2 will see this as the first prompt. \n")
        
        autoMode = input("Automatic mode will make the program not ask you for anything or pause the conversation and will simply run until stopped forcibly. \nDo you want automatic mode? (y/n)")

        messages1.append({"role": "assistant", "content": first_message})
        messages2.append({"role": "user", "content": first_message})
        
        with open(f"sessions/{sessionSelectionStatus}.txt", "w+") as sessionfile:
            print(f"writing session to file sessions/{sessionSelectionStatus}.txt...")
            sessionfile.write(f"\n{model1Name}")
            sessionfile.write(f"\n{model2Name}")
            sessionfile.write(f"\n{system1}")
            sessionfile.write(f"\n{system2}")
            sessionfile.write(f"\n{autoMode}")
            sessionfile.write(f"\n{first_message}")
            sessionfile.write("\n")
            print(f"wrote sessions/{sessionSelectionStatus}.txt succesfully!")


with open("log.txt", "w", encoding="utf-8") as file:
    file.write(f"{model1Name} system: {system1}")
    file.write("\n")
    file.write(f"{model2Name} system: {system2}")
    file.write("\n")    
    file.write(f"{model1Name}: {first_message}")
    file.write("\n")


# Continue the conversation:
user_input = ""
while True:
    if autoMode.lower() == "n":
        user_input = input(f"You (1 to alter {model1_name}'s system, 2 for {model2_name}'s): ")
    if user_input == "/quit":
        print("quitting...")
        break  # exit loop on empty input
    if "1" in user_input:
        new_system = input("new system message for model 1: ")
        messages1.append({"role": "system", "content": new_system})
    elif "2" in user_input:
        new_system = input("new system message for model 2: ")
        messages1.append({"role": "system", "content": new_system})

    print(f"{model2Name} is thinking...")
    model2_response = ollama.chat(model=model2Name, messages=messages2) # generate model2s response
    messages2.append({"role": "assistant", "content": model2_response.message.content})  # add model2s response to model2's context list
    messages1.append({"role": "user", "content": model2_response.message.content})       # add model2s response to model1's context list

    print(f"{model2Name}: ", model2_response.message.content)                           # display model2s response

    print(f"{model1Name} is thinking...")
    model1_response = ollama.chat(model=model1Name, messages=messages1) # generate model2s response
    messages1.append({"role": "assistant", "content": model1_response.message.content})  # add model2s response to model2's context list
    messages2.append({"role": "user", "content": model1_response.message.content}) # add model2s response to model1's context list

    print(f"{model1Name}: ", model1_response.message.content)                           # display model1s response

    print("customsystemmessage1: ", system1)
    
    messages1.append({"role": "system", "content": system1}) # remind models of their system message (i may get ayaw with only mentionning this every few messages but it's staying until it's an issue)
    messages2.append({"role": "system", "content": system2}) # remind models of their system message (i may get ayaw with only mentionning this every few messages but it's staying until it's an issue)
    
    with open("log.txt", "a", encoding="utf-8") as file:
        file.write("\n")
        file.write(f"{model2Name}: {model2_response.message.content}")
        file.write("\n")
        file.write(f"{model1Name}: {model1_response.message.content}")
        file.write("\n")

with open("full_log.txt", "w", encoding="utf-8") as file:
    json.dump(messages2, file)    
    file.write("\n")

print(f"stopping {model1Name}")
ollama.stop("model1Name")
print(f"stopping {model2Name}")
ollama.stop("model2Name")
    
print("quitted successfully!")
