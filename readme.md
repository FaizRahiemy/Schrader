
# Schrader

> "A Guy That Clean Has To Be Dirty." - Hank Schreder

No matter how confident you are before the audit, you may have undeceted issue in your assets. Schrader is an automated tool developed to gather information from VMs and inspect them on whether they complies with the defined requirements or not.

## How to Use

>"It's Easy Money - 'Til We Catch You." - Hank Schrader

It's easy to working as an engineer, until there is an issue/incident occurs. To prevent that happend, Schrader can be used for early detection tool. To use Schrader, the project files need to be put in a server that can access all other VMs that need to be inspected, furthermore, there are several steps before you can run the evaluation tool.

### Set Credentials
There are two ways to store credentials that will be used by Schrader. The first way is to put on a `config.txt` file, and the second way is to put them in environment variables.

#### Config File
Open `config.txt` file and modify below fields:

    username = "[[fill with username]]"
	password = "[[fill with password]]"
	key_file_name = "[[fill with environment]]"
Don't forget to remove the username and password after activity is done to prevent being used by unauthorized party, or set the permission to the file so they cannot access it.

#### Environment Variables
Use below environment variables:

    `SCHRADER_USERNAME` => fill with username
	`SCHRADER_PASSWORD` => fill with password
	`SCHRADER_KEY_FILE` => fill with environment

### Set hosts
Put all IP addresses that required to be evaluated in `inventory.lst` file.

### Package Requirements

	paramiko==3.4.1

### Install Package Requirements

    python3 -m pip install -r requirements.txt

### Run Inspect

    python3 schrader.py -s file -f config.txt -i inventory.lst