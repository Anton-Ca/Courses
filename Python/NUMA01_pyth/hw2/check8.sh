echo ""
echo "Checking task 4"
python3 -c "from hw import *; I1=Interval(1,4); sys.stdout.write(repr(I1)); print(); I2=Interval(-2,-1); sys.stdout.write(repr(I2)); print(); sys.stdout.write(repr(I1+I2)); print(); sys.stdout.write(repr(I1-I2)); print(); sys.stdout.write(repr(I1*I2)); print(); sys.stdout.write(repr(I1/I2)); print('\n')"
