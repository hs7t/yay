from parsing import Parser
from tokenization import Tokenizer

tokens = Tokenizer("""
    % yay 0.1
    % title "Example script"
    % revision 1
    % supports "meow"

    / the following line will print the title we set above!
    ! print meta.title

    ! end
    """).getTokens()

print("\n🔠 Raw tokens:")
for token in tokens:
    print("* ", [(token.type, token.text)])

instructions = Parser(tokens).getInstructions()

print("\n📋 Instructions:")
for instruction in instructions:
    print(
        "- ",
        [
            instruction.commandType,
            instruction.referenceType,
            instruction.reference,
            [[argument.type, argument.value] for argument in instruction.arguments],
        ],
    )

# computerProcess = ComputerProcess()

# print(computerProcess.shell.type)

# computerProcess.stashCommand('echo "Hello, world" > hii.txt')
# computerProcess.stashCommand('echo "Greetings" > salutations.txt')

# computerProcess.runStashedCommands()
