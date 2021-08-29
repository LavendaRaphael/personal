#!/bin/awk -f

BEGIN{
    l0=substr(ARGV[1],1,4);
    mark0=99999999
}{
    i1=index($1,"月");
    i2=index($1,"日");
    if (i1-2>=0 && i1-3<=0 && i2-4>=0 && i2-6<=0){
        l1=substr($1,1,(i1-1));
        l2=substr($1,(i1+1),(i2-i1-1));
        if (l1-10<0){l1=0 l1};
        if (l2-10<0){l2=0 l2};
        mark1=l0 l1 l2
        file=l0"/"l1"/"mark1".txt";
        print file;
        if (mark1-mark0>=0){
            print "exit"
            exit 1
        }
        mark0=mark1;
        #print "["mark1"]\n" > file;
    };
    #print $0"\n" >> file;
}
