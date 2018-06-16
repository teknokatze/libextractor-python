default: guix-environment

guix-environment:
	guix environment -l guix-env.scm --pure

clean:
	rm -rf */*.pyc */*~ *~
