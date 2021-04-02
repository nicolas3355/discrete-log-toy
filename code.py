import random
import time


class PositiveIntegersModP:

    def __init__(self, num, prime):
        if num >= prime or num <= 0:
            error = 'Num {} not in Group range 1 to {}'.format(
                num, prime - 1)
            raise ValueError(error)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return 'GroupElement_{}({})'.format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False
        return self.num == other.num and self.prime == other.prime

    def __mul__(self, other):
        # override the "*" symbol with our multiplication
        if self.prime != other.prime:
            raise TypeError('Cannot multiply two numbers in different Groups')
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)

        # does repeated squaring inside
        def my_pow(base, exp):
            # exponentiation by repeated squaring
            # order of magnitude more efficient than naive_my_pow
            # O(log(exp))
            p = self.prime
            if exp == 0:
                return 1
            elif exp == 1:
                return base % p
            elif exp % 2 == 0:
                return my_pow(base * base, exp / 2) % p
            else:
                return (base * my_pow(base * base, (exp - 1) / 2)) % p

        num = my_pow(self.num, n)
        return self.__class__(num, self.prime)

    def __hash__(self):
        # i added this so i can use set operations
        return hash((self.num, self.prime))


def time_func(f):
    start = time.time()
    f()
    end = time.time()
    print(end - start)

# taking an example:
# print("the multiplicative group of integers mod 7")
# print([i for i in range(1, 7)])
# i claim that 3 is a generator of that group
# i can generate all the other elements using 3 and the binary operation of
# multiplication

def list_elements_from_3():
    elems = [PositiveIntegersModP(3, 7)]
    elem = PositiveIntegersModP(3, 7)
    for i in range(1, 6):
        elem = elem * PositiveIntegersModP(3, 7)
        elems.append(elem)
    return elems
# print(list_elements_from_3())


# G = 3, 3*3 % 7, (3*3*3) % 7, (3*3*3*3)%7, (3*3*3*3*3)%7, (3*3*3*3*3*3)%7, (3*3*3*3*3*3*3)%7
# G = (3**6) % 7, (3**0) % 7, (3**1) % 7, (3**2) % 7, (3**3) % 7, (3**4) % 7, (3**5) % 7 
# G = (3**i) % 7 for all i


def list_elements_from_3_pow():
    elems = []
    elem = PositiveIntegersModP(3, 7)
    for i in range(0, 6):
        elems.append(elem ** i)
    return elems

# print(list_elements_from_3_pow())
# g = PositiveIntegersModP(3, 7)


def is_naive_generator(g):
    # check if an element is a generator by generating all elements
    # from it and see if we covered all the elements in the Group.
    # the number of elements in the Group should be prime - 1.
    # the order of the Group is prime - 1.
    elems = set()
    for i in range(0, g.prime - 1):
        elems.add(g ** i)
    return len(elems) == (g.prime - 1)

# assert(is_naive_generator(g))


def get_naive_generator(prime):
    # go over all elements in the finite Group and check each element
    # one by one if it's a generator. returns the first element
    # it finds
    for i in range(1, prime):
        if(is_naive_generator(PositiveIntegersModP(i, prime))):
            return PositiveIntegersModP(i, prime)

# g2 = get_naive_generator(7)
# print("getting a generator for the multiplicative group of integers mod 7:\n",
#      g)

# assert(g == g2)


def list_elements_from_generator(g: PositiveIntegersModP):
    # By definition a generator should be able to generate all the
    # elements in the finite Group. Let's return this list.
    assert is_naive_generator(g)
    elems = []
    for i in range(0, g.prime - 1):
        elems.append(g ** i)
    assert(len(elems) == g.prime - 1)
    return elems

# print (list_elements_from_generator(g))


# -----------------------------------------------------------------------------------
# exponentiation

#a**b = (a * a* a *...) there is going to b a. and b-1 mutiplictions
# 2**3 = 2*2*2

def naive_my_pow(base, exp):
    # exponentiate the most naive way
    # by multiplying base by itself (exp - 1) times
    # O(exp)
    if exp == 0:
        return 1
    res = base
    for i in range(1, exp):
        res = res * base
    return res

# test it on 2**21
#assert(naive_my_pow(2, 21) == 2**21)
#print(naive_my_pow(2, 21))

# very slow
# number of multiplications are linear in exp

#print(naive_my_pow(2, 2**28))
# if we have something like 3**64 can we compute it in a quicker way
#  3**64    = (3 * 3) ** 32
#           = (9 * 9) ** 16
#           = (81 * 81) ** 8
#           = (6561 * 6561) ** 4
#           = (43046721 * 43046721) ** 2
#           = (1853020188851841 * 1853020188851841)
#           6 multiplications in total instead of 63 multiplication using the naive method

# this cost 6 mult instead of 64, Log2(64) mult
# this worked because the exponent 64 is power of 2
# what if it's not !!
# well let's express it in terms of power of 2.


# 2**7
# 2**7 = 2* 2**2 * 2**4
# It's exactly bin(exp)
# print(bin(7))
# Let's take an example 2**7
# 7 in binary is 111
# 3**7 = 3 * 3**2 * 3**4


# 3**7 = 3 * ((3 * 3) ** 3)
#      = 3 * ( 9 * ((9 * 9) ** 1.0))
#      = 3 * 9 * 81
#      = 3 * (3**2) * (3**4)
# total amount of multiplication in this case = 2 + 1 + 1 instead of 6

# 3**100 = 3**4 * 3**32 * 3 ** 64 => total mutls = 2 + 2 + 3 + 1 = 8 instead of 99

# print("measuring time for the naive_my_pow")
# time_func(lambda: naive_my_pow(base, exp))
def my_pow(base, exp):
    # exponentiation by repeated squaring
    # order of magnitude more efficient than naive_my_pow
    # O(log(exp)) number of mults
    if exp == 0:
        return 1
    elif exp == 1:
        return base
    elif exp % 2 == 0:
        return my_pow(base * base, exp / 2)
    else:
        return base * my_pow(base * base, (exp - 1) / 2)

# base = 2
# exp = 2**20

# print("measuring time for the improved my_pow")
# a = my_pow(base, exp)
# print(a)
# time_func(lambda: my_pow(base, exp))


# -----------------------------------------------
# log begins

# discret log: given A get x such that A = g ^ x


# G = 2, 2*2, 2*2*2, 2*2*2*2....
# G = 2**0, 2**1, 2**2 ....
# G = 2**i  for all i between 0 and infinity

# listing 2**i for all i between 0 30
# print([(2)**i for i in range(0, 31)])


# print(2 ** (2 ** 30))

def naive_log(n, base):
    res = base
    index = 1
    while res != n:
        res = res * base
        index += 1
    return index

# print(naive_log(2**10, 2))
# assert(naive_log(2**10, 2) == 10)


# print(naive_log(2**(2**28), 2))

def helper_log(n, base):
    # find the min and max possible exponent
    # helper for binary_search_log
    # returns true if exp happens to be the exact exponent
    total = base
    exp = 1
    while (total * total <= n):
        total = total * total
        exp = exp * 2
    if n == total:
        return exp, True
    else:
        return exp, False


def binary_search_log(n, base):
    # this log assumes base^x = n where x is an integer
    # doesn't work in ourGroup
    # exploits the fact that base^x is always increasing with
    # x. forall x, base ^ (x) < base ^ (x+1}).
    current_index, res = helper_log(n, base)
    if(res):
            return current_index

    L = current_index
    R = current_index * 2
    while L <= R:
        mid = (L+R)//2
        array_mid = my_pow(base, mid)
        if array_mid < n:
            L = mid + 1
        elif array_mid > n:
            R = mid - 1
        else:
            return mid
    return -1


# exploiting the structure:
# log_value = binary_search_log(2**(2**28), 2)
# assert(log_value == 2**28)
# print(time_func(lambda: binary_search_log(2**(2**28), 2)))
# print(binary_search_log(17**8711, 17))


# g = get_naive_generator(23)
# print(g)
# print(list_elements_from_generator(g))
# print([(g.num)**i for i in range(0, g.prime)])


# DHE
def DHE():
    print("-------Diffie–Hellman key exchange--------")
    print("------------------------------------------")
    print("------------------------------------------")
    print("------------------------------------------")
    print("------------------------------------------")
    print("------------------------------------------")
    # DHE is defined over finite cyclic multiplicative groups
    # where Discrete Log is assumed to hard.
    # we are going to pick the integers mod 23 with the operation of *.
    # prime numbers p and q along with the group generators are known
    # and are assumed to be public.
    q = 11
    p = (2 * q) + 1  # p is a safe prime
    g = get_naive_generator(p)
    print(list_elements_from_generator(g))

    def genkey():
        # pick a random exponent for g in the quadratic residue of the group
        # formed by the prime number p (Search for Euler’s Criterion).
        # this is chosen this way for Decisional Diffie Helman to hold.
        # g, g**a, g**b, g**ab indistinguishable from g, g**a, g**b, g**c
        # our secret is hidden in q numbers in this case 10 numbers
        secret_key = random.randint(0, q) * 2
        public_key = g**secret_key
        return secret_key, public_key

    # We are going simulate the communication between alice and bob
    # I defined bob inside alice for simplicity, alice will pass her public
    # key to bob through a function call to the bob function, the bob function
    # will return bob's public key.
    # an attacker who has access to alice's pk g**a can not compute a
    # because of the assumption that the discrete log is hard.
    # an attacker who has access to Bob's pk g**b can not compute b
    # also because of the dicrete log problem.
    # an attacker who has access g**a, g**b and g can not compute g**ab
    # Computational Diffie-Hellman problem
    # g**ab is considered be a good symmetric key because of Decisional Diffie
    # Helman (DDH).
    # DDH g**a, g**b, g**ab is indistinguishable from g**a, g**b, g**r
    # where a , b and r are picked uniformly at random from the big group G

    def alice():
        # generate public key and secret key
        sk, pk_alice = genkey()
        print("alice's secret key: ", sk)
        print("alice's public key: ", pk_alice)
        print("-------------------------")

        def bob(get_alice_pk):
            # bob repeating the same steps as alice
            sk, pk = genkey()
            print("Bob 's secret key: ", sk)
            print("Bob 's public key: ", pk)
            print("-------------------------")
            pk_alice = get_alice_pk()
            symmetric_key = pk_alice ** sk
            print("symmetric key bob: ", symmetric_key)
            return pk

        # send's bob her own public key and wait for his public key
        pk_bob = bob(lambda: pk_alice)
        # Alice has bob's public key she can now compute the secret
        # symmetric key
        symmetric_key = pk_bob ** sk
        print("symmetric key alice: ", symmetric_key)
        return pk_alice, pk_bob

    pk_alice, pk_bob = alice()

    def compute_symmetric_key_from_pks():
        # breaking one of the pks is enough to recover the shared secret
        # we know both g**a, and g**b we need to compute g**ab
        # we are a very powerful attacker that can break discrete log
        # in this very big group!.
        elems = list_elements_from_generator(g)
        # let's recover alice's private key using her public key
        a = elems.index(pk_alice)
        # compute symmetric key g**ab
        cracked_symmetric_key = pk_bob ** a
        print("cracked symmetric key", cracked_symmetric_key)
    # compute_symmetric_key_from_pks()

# DHE()
