# smllibs

This is a lackluster library I wrote that helps with writing SML style hw in python

#set up based on this guide https://medium.com/analytics-vidhya/how-to-create-a-python-library-7d5aea80cc3f

#function discriptions found here
https://www.diderot.one/courses/44/books/261/part/435/chapter/3077




#################
The SEQUENCE signature is a comprehensive interface for a persistent sequence type.

1
Summary
signature SEQUENCE =  
sig  
  type 'a t  
  type 'a seq = 'a t  
  type 'a ord = 'a * 'a -> order  
  datatype 'a listview = NIL | CONS of 'a * 'a seq  
  datatype 'a treeview = EMPTY | ONE of 'a | PAIR of 'a seq * 'a seq  
  
  exception Range  
  exception Size  
  
  val nth : 'a seq -> int -> 'a  
  val length : 'a seq -> int  
  val toList : 'a seq -> 'a list  
  val toString : ('a -> string) -> 'a seq -> string  
  val equal : ('a * 'a -> bool) -> 'a seq * 'a seq -> bool  
  
  val empty : unit -> 'a seq  
  val singleton : 'a -> 'a seq  
  val tabulate : (int -> 'a) -> int -> 'a seq  
  val fromList : 'a list -> 'a seq  
  
  val rev : 'a seq -> 'a seq  
  val append : 'a seq * 'a seq -> 'a seq  
  val flatten : 'a seq seq -> 'a seq  
  
  val filter : ('a -> bool) -> 'a seq -> 'a seq  
  val map : ('a -> 'b) -> 'a seq -> 'b seq  
  val zip : 'a seq * 'b seq -> ('a * 'b) seq  
  val zipWith : ('a * 'b -> 'c) -> 'a seq * 'b seq -> 'c seq  
  
  val enum : 'a seq -> (int * 'a) seq  
  val filterIdx : (int * 'a -> bool) -> 'a seq -> 'a seq  
  val mapIdx : (int * 'a -> 'b) -> 'a seq -> 'b seq  
  val update : 'a seq * (int * 'a) -> 'a seq  
  val inject : 'a seq * (int * 'a) seq -> 'a seq  
  
  val subseq : 'a seq -> int * int -> 'a seq  
  val take : 'a seq -> int -> 'a seq  
  val drop : 'a seq -> int -> 'a seq  
  val splitHead : 'a seq -> 'a listview  
  val splitMid : 'a seq -> 'a treeview  
  
  val iterate : ('b * 'a -> 'b) -> 'b -> 'a seq -> 'b  
  val iteratePrefixes : ('b * 'a -> 'b) -> 'b -> 'a seq -> 'b seq * 'b  
  val iteratePrefixesIncl : ('b * 'a -> 'b) -> 'b -> 'a seq -> 'b seq  
  val reduce : ('a * 'a -> 'a) -> 'a -> 'a seq -> 'a  
  val scan : ('a * 'a -> 'a) -> 'a -> 'a seq -> 'a seq * 'a  
  val scanIncl : ('a * 'a -> 'a) -> 'a -> 'a seq -> 'a seq  
  
  val sort : 'a ord -> 'a seq -> 'a seq  
  val merge : 'a ord -> 'a seq * 'a seq -> 'a seq  
  val collect : 'a ord -> ('a * 'b) seq -> ('a * 'b seq) seq  
  val collate : 'a ord -> 'a seq ord  
  val argmax : 'a ord -> 'a seq -> int  
  
  val $ : 'a -> 'a seq  
  val % : 'a list -> 'a seq  
end  
2
Types
type 'a t  
type 'a seq = 'a t  
The abstract sequence type ’a t has elements of type ’a. The alias ’a seq is for readability.

type 'a ord = 'a * 'a -> order  
An alias, for readability.

datatype 'a listview = NIL | CONS of 'a * 'a seq  
View a sequence as though it were a list. See splitHead.

datatype 'a treeview = EMPTY | ONE of 'a | PAIR of 'a seq * 'a seq  
View of a sequence as though it were a tree with data at the leaves. This is largely a syntactic convenience for 2-way divide-and-conquer algorithms on sequences. See splitMid.

3
Exceptions
exception Range  
The Range exception is raised whenever an invalid index into a sequence is used.

exception Size  
The Size exception is raised whenever a function is given a negative size.

4
Values
nth
val nth : 'a seq -> int -> 'a  
nth s i evaluates to s[i], the ith element of s. Raises Range if i is out-of-bounds.

length
val length : 'a seq -> int  
length s evaluates to |s|, the number of elements in s.

toList
val toList : 'a seq -> 'a list  
Produces an index-preserving list representation of a sequence.

val toString : ('a -> string) -> 'a seq -> string  
toString f s produces a string representation of s, where each element of s is converted to a string via f.

toString Int.toString (fromList [1,2,3]) evaluates to "<1,2,3>".

equal
val equal : ('a * 'a -> bool) -> 'a seq * 'a seq -> bool  
equal f (s, t) returns whether or not s and t contain equal elements in the same order. Individual element pairs are compared for equality with f.

empty
val empty : unit -> 'a seq  
Construct an empty sequence.

singleton
val singleton : 'a -> 'a seq  
singleton x evaluates to ⟨x⟩.

tabulate
val tabulate : (int -> 'a) -> int -> 'a seq  
tabulate f n evaluates to the length-n sequence where the ith element is given by f(i). Raises Size if n<0.

fromList
val fromList : 'a list -> 'a seq  
Produces an index-preserving sequence from a list.

rev
val rev : 'a seq -> 'a seq  
rev s reverses the indexing of a sequence. That is, nth (rev s) i is equivalent to nth s (length s - i - 1).

append
val append : 'a seq * 'a seq -> 'a seq  
Concatenate two sequences.

flatten
val flatten : 'a seq seq -> 'a seq  
Concatenate many sequences into one, in the order they are given.

Example
Flattening ⟨⟨1,2⟩,⟨⟩,⟨3⟩⟩ results in ⟨1,2,3⟩.

filter
val filter : ('a -> bool) -> 'a seq -> 'a seq  
filter p s evaluates to the subsequence of s which contains every element satisfying the predicate p.

map
val map : ('a -> 'b) -> 'a seq -> 'b seq  
map f s applies f to each element of s. It is logically equivalent to tabulate (f o nth s) (length s).

zip
val zip : 'a seq * 'b seq -> ('a * 'b) seq  
zip (s, t) evaluates to a sequence of length min(|s|,|t|) whose ith element is the pair (s[i],t[i]).

zipWith
val zipWith : ('a * 'b -> 'c) -> 'a seq * 'b seq -> 'c seq  
zipWith f (s, t) is logically equivalent to map f (zip (s, t)).

enum
val enum : 'a seq -> (int * 'a) seq  
enum s evaluates to a sequence where each element is paired with its index. It is logically equivalent to tabulate (fn i => (i, nth s i)) (length s).

filterIdx
val filterIdx : (int * 'a -> bool) -> 'a seq -> 'a seq  
Similar to filter, but also provides the index of each element to the predicate. filterIdx f s is logically equivalent to map (fn (_, x) => x) (filter f (enum s)).

mapIdx
val mapIdx : (int * 'a -> 'b) -> 'a seq -> 'b seq  
Similar to map, but also provides the index of each element. mapIdx f s is logically equivalent to map f (enum s).

update
val update : 'a seq * (int * 'a) -> 'a seq  
update (s, (i, x)) evaluates to the sequence whose ith element is x, and whose other elements are unchanged from s. If i is out-of-bounds, it raises Range, otherwise it is logically equivalent to tabulate (fn j => if i = j then x else nth s j) (length s).

val inject : 'a seq * (int * 'a) seq -> 'a seq  
inject (s, u) produces a new sequence where, for each (i,x)∈u, the ith element of s has been replaced with x. If there are multiple updates specified at the same index, then all but one of them are ignored non-deterministically. Raises Range if any (i,_)∈u is out-of-bounds.

When all indices in u are distinct, inject (s, u) is logically equivalent to iterate update s u.

subseq
val subseq : 'a seq -> int * int -> 'a seq  
subseq s (i, n) evaluates to the contiguous subsequence of s starting at index i with length n. Raises Size if n<0. Raises Range if the subsequence is out-of-bounds.

take
val take : 'a seq -> int -> 'a seq  
take s n takes the prefix of s of length n. It is logically equivalent to subseq s (0, n).

drop
val drop : 'a seq -> int -> 'a seq  
drop s n drops the prefix of s of length n. It is logically equivalent to subseq s (n, length s - n).

splitHead
val splitHead : 'a seq -> 'a listview  
splitHead s evaluates to NIL if s is empty, and otherwise is logically equivalent to CONS (nth s 0, drop s 1).

splitMid
val splitMid : 'a seq -> 'a treeview  
splitMid s evaluates to EMPTY is s is empty, ONE x if s=⟨x⟩, and PAIR (l, r) otherwise where l and r are non-empty and their concatenation is s. The sizes of l and r are implementation-defined.

val iterate : ('b * 'a -> 'b) -> 'b -> 'a seq -> 'b  
iterate f b s computes the iteration of f on s with left-association, using b as the base case. It is logically equivalent to
f(…f(f(b,s[0]),s[1])…,s[|s|−1])

When s is empty, it returns b.

iterate op+ 13 (fromList [1,2,3]) evaluates to 19.

iteratePrefixes
val iteratePrefixes : ('b * 'a -> 'b) -> 'b -> 'a seq -> 'b seq * 'b  
iteratePrefixes f b s is logically equivalent to
(tabulate (fn i => iterate f b (take s i)) (length s), iterate f b s).
That is, it produces the iteration of f for each prefix of s.

val iteratePrefixesIncl : ('b * 'a -> 'b) -> 'b -> 'a seq -> 'b seq  
Similar to iteratePrefixes, except that the ith prefix of iteratePrefixesIncl f b s is inclusive of s[i], rather than exclusive. It is logically equivalent to
tabulate (fn i => iterate f b (take s (i+1)) (length s).

The return type of iteratePrefixesIncl is slightly different than iteratePrefixes.

val reduce : ('a * 'a -> 'a) -> 'a -> 'a seq -> 'a  
reduce f b s evaluates to b when s=⟨⟩, x when s=⟨x⟩, and otherwise is logically equivalent to
f (reduce f b l, reduce f b r)
where l=take s (n div 2) and r=drop s (n div 2).

reduce f b s is logically equivalent to iterate f b s when f is associative and b is a corresponding identity.

scan
val scan : ('a * 'a -> 'a) -> 'a -> 'a seq -> 'a seq * 'a  
For an associative function f and corresponding identity b, scan f b s is logically equivalent to iteratePrefixes f b s.

scanIncl
val scanIncl : ('a * 'a -> 'a) -> 'a -> 'a seq -> 'a seq  
For an associative function f and corresponding identity b, scanIncl f b s is logically equivalent to iteratePrefixesIncl f b s.

sort
val sort : 'a ord -> 'a seq -> 'a seq  
sort c s reorders the elements of s with respect to the comparison function c. The output is stable: any two elements considered equal by c will appear in the same relative order in the output as they were in the input.

merge
val merge : 'a ord -> 'a seq * 'a seq -> 'a seq  
For sequences s and t already sorted with respect to c, merge c (s, t) is logically equivalent to sort c (append (s, t)).

val collect : 'a ord -> ('a * 'b) seq -> ('a * 'b seq) seq  
collect c s takes a sequence s of key-value pairs, deduplicates the keys, sorts them with respect to c, and pairs each unique key with all values that were originally associated with it in s. The resulting value-sequences retain their relative ordering from s.

Collecting ⟨(3,7),(2,6),(1,8),(3,5)⟩ produces ⟨(1,⟨8⟩),(2,⟨6⟩),(3,⟨7,5⟩)⟩.

collate
val collate : 'a ord -> 'a seq ord  
collate c produces an ordering on sequences, derived lexicographically from c.

argmax
val argmax : 'a ord -> 'a seq -> int  
argmax c s produces the index of the maximal value in s with respect to c. Raises Range when s is empty.

$
val $ : 'a -> 'a seq  
An alias for singleton.

%
val % : 'a list -> 'a seq  
An alias for fromList.
##############
