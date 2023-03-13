U, A, S = "user", "assistant", "system"


help_prompt_math : str = """\
The user needs help on some tasks. 
It is important you do not output the answer outright.
Rather, you should reason deeply, step by step,
and only then produce the final answer in the last few tokens, 
in the form [Answer] {'ans' : ...}.""" 


example_shot_aime_points : dict[str, str] = {
    "user": """\
Example:
[Q] Twenty distinct points are marked on a circle and labeled $1$ through $20$ in clockwise order.
A line segment is drawn between every pair of points whose labels differ by a prime number.  
Find the number of triangles formed whose vertices are among the original $20$ points.
[Format] INTEGER.
""",
    "assistant": """\
Suppose $i$, $j$, and $k$ are the labels of the three vertices of a triangle; without loss, let $i > j > k$.
Note that $(i-j) + (j-k) = (i-k)$, so one of $i-j$ or $j-k$ must be $2$, and furthermore the other two primes must be twin primes.  
A quick count reveals that \[(i-j,j-k,i-k)\in\{(2,3,5),(2,5,7),(2,11,13),(2,17,19)\}\] and permutations
where the first two coordinates are swapped. In particular, for any pairs of vertices $(a,a+d)$,
where $d\in\{5,7,13,19\}$, there are exactly two locations for the middle vertex which yield a triangle.
Finally, observe that there are $20-d$ pairs of vertices $(a,a+d)$ for every $d$ between $1$ and $19$.
Summing over all $d$ gives an answer of $2(15+13+7+1) = \\boxed{72}$.

[Answer] {'ans' : 72}"""
}


