from smali.shell import ISmaliShell, start_cli

# Just start the shell in your code or
# call it from the CLI with 'python3 -m smali.shell'
shell = ISmaliShell()

# disable import checks so that recursive imports are 
# possible (NOT recommended and disabled by default)
shell.check_import = False
shell.cmdloop()

# Or just call start CLI
start_cli()
