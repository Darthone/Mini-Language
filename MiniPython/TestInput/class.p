class list(init)
    L := init;
    z := 11;
 
    define Cons proc(x) 
        L := cons x, L; 
        return := L;
    end;

    define Car proc() 
        return := car L; 
    end;

    define Cdr proc() 
        return := cdr L; 
    end;
end;

L := new list([]);
T := L.Cons(3);
T := L.Cons(2);
T := L.Cons(1);
x := L.Car();
M := L.Cdr();
q := L.z;
p := L.L;


