
def inc = \n.\f.\z. f (n f z);
def _0 = \f.\z. z;
def _1 = inc _0;
def _2 = inc _1;

def sum = \n.\m. n inc m;
def value = \n. n (\x. + x 1) 0;
def eq = \x.\y. ifz (- x y) 1 0;
def is_div = \x.\y. eq (* (/ x y) y) x;

def v1 = value _1;
def v2 = value _2;
def v3 = value (sum _2 _1);
def v4 = value (sum _2 _2);
def v5 = value (sum (sum _2 _1) _2);

def t1 = is_div 6 (value _2);
def f1 = is_div 4 3;
def t2 = is_div 1 1;
def f2 = is_div 9 8;