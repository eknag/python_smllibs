from smllibs import Seq

def test_nth():
    s = [0,1,2,3,4]
    for v in s:
        assert(v == Seq.nth(s)(v))
        print("good")
    print("nth good")


test_nth()