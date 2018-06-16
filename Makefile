default: guix-environment

guix-environment:
	guix environment -l guix-env.scm --pure

run:
	./arrr python2 examples/extract.py README

clean:
	rm -rf */*.pyc */*~ *~
