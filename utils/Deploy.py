import os , json 
from solcx import compile_standard, install_solc
install_solc('0.8.0')
print(os.getcwd())

# Changin path to src/contracts 
# Our file lives @  E:\Backup\Area_51\Implicit\Solidity\Cre-Own


os.chdir("src/contracts/")
print(os.getcwd())
print(os.listdir())

with open("interface.sol", "r") as file:
    contact_list_file = file.read()
    print(contact_list_file)

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"ContactList.sol": {"content": contact_list_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"] # output needed to interact with and deploy contract 
                }
            }
        },
    },
    solc_version="0.8.0",
)
print(compiled_sol)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
