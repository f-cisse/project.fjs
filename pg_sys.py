""" Les processus (fork()) """
# permet de cree un processus fils a partir d'un processus pere, 
# le processus fils est une copie du processus pere, il herite de son environnement et de ses variables. 

""" il nous faut importer la blibliopteque  'os' , celle ci permet 
de gere les signaux , les processus, acceder au systeme de  fichiers, gere les groupe et les utilisateurs"""

"""Le module sys est un module natif de Python qui permet d'interagir
 directement avec l'interpréteur et l'environnement d'exécution """

""" Le module natif shlex  permet de découper et sécuriser des 
chaînes de caractères comme le ferait un terminal Unix"""
import sys
import os
import shlex
import time 
# rappel: pid = id du processus, et ppid = parent du pid précédent
#pid = os.getpid()
#ppid = os.getppid() 
#print( "je suis le processus", pid, "et mon pere est", ppid)
#time.sleep(15)
"""_____________________________________________________________________________________________________________________"""

ALIASES = {  # commande opsh demander dans lennoncé du projet et leur equivalent 
    'list': 'ls',
    'show': 'cat',
    'copy': 'cp',
    'move': 'mv',
    'del': 'rm',
    'newdir': 'mkdir',
    'newfile': 'touch',
}
# Si la commande tapée est un alias, on remplace args[0] par la vraie commande
if args[0] in ALIASES:
    args[0] = ALIASES[args[0]]

"""____________________________________________________________________________________________________________________________"""

def pipeline_fork(commandes):
    nb_cmds = len(commandes)  # 
    pids = []
    input_file = 0  # Entrée standard initiale (stdin = 0)

    for i, cmd_str in enumerate(commandes):
        # Découpage sécurisé des arguments (gère les guillemets)
        args = shlex.split(cmd_str.strip())
        if not args:
            continue
    
        # Gestion des commandes internes (built-ins)
        if args[0] == "exit":
            sys.exit(0)
        if args[0] == "go":
            try:
                os.chdir(args[1] if len(args) > 1 else os.path.expanduser("~"))
            except Exception as e:
                print(f"opsh: go: {e}", file=sys.stderr)
            return
        # quit remplace exit
        elif args[0] == "quit":
            sys.exit(0)
        # path remplace pwd
        elif args[0] == "path":
            print(os.getcwd())
        # say remplace echo
        elif args[0] == "say":
            print(" ".join(args[1:]))
        # osinfo spécifique au TP
        elif args[0] == "osinfo":
            print("Systèmes d'Exploitation -- UIR/ESIN")




        # Création d'un pipe sauf pour la dernière commande
        if i < nb_cmds - 1:
            read_fd, write_fd = os.pipe()
        else:
            read_fd, write_fd = None, None

        try : # verifier si le fork() a reussi ou pas, si il a reussi il retourne 0 pour le processus fils et le pid du processus fils pour le processus pere, sinon il retourne -1.
            pid= os.fork() # cree un processus fils
        except OSError:
            print("erreur de la commande fork()")
            sys.exit(-1)

        if pid == 0:
            # processus fils
            # 1. Redirection de l'entrée depuis la commande précédente
            if input_file != 0:
                os.dup2(input_file, 0)
                os.close(input_file)

            # 2. Redirection de la sortie vers la commande suivante
            if write_fd is not None:
                os.dup2(write_fd, 1)
                os.close(write_fd)
                os.close(read_fd)


            # 3. Exécution du binaire
            try:
                os.execvp(args[0], args)
            except FileNotFoundError:
                print(
                    f"opsh: commande introuvable : {args[0]}", file=sys.stderr
                )
                os._exit(127)
            except Exception as e:
                print(f"opsh: erreur d'exécution : {e}", file=sys.stderr)
                os._exit(1)
        else:
            # --- PROCESSUS PARENT ---
            pids.append(pid)

            # Fermeture des descripteurs inutiles dans le parent
            if input_file != 0:
                os.close(input_file)
            if write_fd is not None:
                os.close(write_fd)

            # L'entrée de la prochaine commande sera la sortie de celle-ci
            input_file = read_fd

    # Attente de la fin de tous les processus enfants
    for pid in pids:
        os.waitpid(pid, 0)


def repl():
    while True:
        try:
            # 1. Prompt & Lecture
            entree = input("opsh> ").strip()
            if not entree:
                continue

            # 2. Découpage par '->'
            commandes = entree.split("->")

            # 3. Exécution
            executer_pipeline_fork(commandes)

        except EOFError:  # Gestion de Ctrl+D
            print()
            break
        except KeyboardInterrupt:  # Gestion de Ctrl+C
            print()
            continue


if __name__ == "__main__":
    repl()







""" ____________________________________________________________________"""
try : # verifier si le fork() a reussi ou pas, si il a reussi il retourne 0 pour le processus fils et le pid du processus fils pour le processus pere, sinon il retourne -1.
    p= os.fork() # cree un processus fils
except OSError:
    print("erreur de la commande fork()")
    sys.exit(-1)
if p==0: # processus fils
    print("je suis le processus fils", os.getpid(), "et mon pere est", os.getppid())
else:
    print("je suis le processus pere", os.getpid(), "et mon fils est", p)