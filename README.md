    This is just test^_^
    Example:
    1> Add or update rpm.db
       # getRPM.py -u http://mirror.centos.org/centos/6/os/x86_64/Packages/
    2> Find  centos6 packages download links include 'python' from rpm.db
       # getRPM.py -v 6 -q python
    3> Write the results to result.txt
       # getRPM.py -v 6 -q query -t result.txt
    4> Read query packages from wanted.txt
       # getRPM.py -v 6 -f wanted.txt
