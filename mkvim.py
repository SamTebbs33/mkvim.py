import argparse, shutil, os

parser = argparse.ArgumentParser(description="Create a vim profile")
parser.add_argument("profile_name", metavar="name", type=str, help="the name of the profile to generate")
# parser.add_argument("-c", "--clean", help="clean all previously made aliases", action="store_true")
parser.add_argument("--vimrc-template", help="alternative vimrc template file (default \'vimrc_template\')", type=str, metavar="file", default="vimrc_template")
parser.add_argument("--vim-template", help="alternative vim template directory (default \'vim_template\')", type=str, metavar="dir", default="vim_template")
parser.add_argument("--aliases", help="file to write the new alias to (default \'~/.vim_aliases\')", type=str, metavar="file", default="~/.vim_aliases")
parser.add_argument("--prefix", help="alias shell command (default \'alias\')", default="alias")
parser.add_argument("--suffix", help="string to place in between alias name and value (default \'=\')", default="=")

# Set variables corresponding to arguments
args = parser.parse_args()
profile_name = args.profile_name
vim_template = args.vim_template
vimrc_template = args.vimrc_template
vim_aliases = args.aliases
alias_prefix = args.prefix
alias_suffix = args.suffix

# Default vimrc_template contents
vimrc_default = '\" It is recommended that you don\'t change the next 3 lines, as they make vim point to your profile\'s .vim directory\n\
let &runtimepath = printf(\'%s/vimfiles,%s,%s/vimfiles/after\', $VIM, $VIMRUNTIME, $VIM)\n\
let s:portable = expand(\'<sfile>:p:h\')\n\
let &runtimepath = printf(\'%s,%s,%s/after\', s:portable, &runtimepath, s:portable)\n\
\" Add anything below this line that you want to be common to all new profiles\n\
set number'

# Create templates if they don't exist
if not os.path.exists(vim_template):
    os.makedirs(vim_template)
if not os.path.exists(vimrc_template):
    f = open(vimrc_template, "w+")
    f.write(vimrc_default)
    f.close()
if not os.path.exists(vim_aliases):
    open(vim_aliases, "w+")
if not os.path.exists(profile_name):
    os.makedirs(profile_name)

print("Making profile: " + profile_name)

# Write alias
dir_path = os.path.dirname(os.path.realpath(__file__))
vim_path = dir_path + "/" + profile_name + "/.vim"
vimrc_path = vim_path + "/.vimrc"
with open(vim_aliases, "a") as file:
    alias = alias_prefix + " vim_" + profile_name + alias_suffix + "\"vim -u " + vimrc_path + "\""
    file.write(alias + "\n")

# cd into new directory and create necessary files
os.chdir(profile_name)
if not os.path.exists(".vim"):
    os.makedirs(".vim")
    shutil.copytree("../" + vim_template, ".vim")

shutil.copyfile("../" + vimrc_template, ".vim/.vimrc")