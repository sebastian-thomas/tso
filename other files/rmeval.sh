for i in {1..10}
do
	perl /home/seb/soft/rogue/ROUGE-1.5.5.pl -e /home/seb/soft/rogue/data -f A -a -x -s -m -2 -4 -u /home/seb/proj/obj/eval/settings$((i)).xml
done