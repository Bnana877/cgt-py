import csv
from graphviz import Digraph
import math


class f_dec:
    def __init__(self, value_, exp_):
        if value_ == 0:
            self.value = 0
            self.exp = 0
        else:
            if exp_ > 0:
                while value_ % 2 == 0:
                    value_ = value_ // 2
                    exp_ -= 1
            if exp_ < 0:
                value_ = value_ * 2 ** (-exp_)
                exp_ = 0
            self.value = value_
            self.exp = exp_

    def __repr__(self):
        return f"({self.value}, {self.exp})"

    def __float__(self):
        return float(self.value) * 2 ** (-self.exp)

    def __str__(self):
        if self.exp == 0:
            return str(self.value)
        return str(float(self))

    def __add__(self, other):
        if self.exp == other.exp:
            return f_dec(self.value + other.value, self.exp)
        elif self.exp > other.exp:
            new_other_value = other.value * 2 ** (self.exp - other.exp)
            return f_dec(self.value + new_other_value, self.exp)
        else:
            new_self_value = self.value * 2 ** (other.exp - self.exp)
            return f_dec(new_self_value + other.value, other.exp)

    def __sub__(self, other):
        if self.exp == other.exp:
            return f_dec(self.value - other.value, self.exp)
        elif self.exp > other.exp:
            new_other_value = other.value * 2 ** (self.exp - other.exp)
            return f_dec(self.value - new_other_value, self.exp)
        else:
            new_self_value = self.value * 2 ** (other.exp - self.exp)
            return f_dec(new_self_value - other.value, other.exp)

    def __mul__(self, other):
        return f_dec(self.value * other.value, self.exp + other.exp)

    def __truediv__(self, other):
        return f_dec(self.value / other.value, self.exp - other.exp)

    def __eq__(self, other):
        if type(other) != f_dec:
            return False
        return self.value == other.value and self.exp == other.exp

    def __lt__(self, other):
        if self.exp == other.exp:
            return self.value < other.value
        elif self.exp > other.exp:
            new_other_value = other.value * 2 ** (self.exp - other.exp)
            return self.value < new_other_value
        else:
            new_self_value = self.value * 2 ** (other.exp - self.exp)
            return new_self_value < other.value

    def __gt__(self, other):
        if self.exp == other.exp:
            return self.value > other.value
        elif self.exp > other.exp:
            new_other_value = other.value * 2 ** (self.exp - other.exp)
            return self.value > new_other_value
        else:
            new_self_value = self.value * 2 ** (other.exp - self.exp)
            return new_self_value > other.value

    def __le__(self, other):
        return self < other or self == other

    def __ge__(self, other):
        return self > other or self == other

    def copy(self):
        return f_dec(self.value, self.exp)


def birthday(num):
    if num.value == 0:
        return 0
    return math.ceil(float(num)) + num.exp


def between_dec(num1, num2):
    if num1 is None:
        return f_dec(min(math.ceil(num2) - 1, 0), 0)
    if num2 is None:
        return f_dec(max(math.floor(num1) + 1, 0), 0)
    max_exp = max(birthday(num1), birthday(num2))
    d_list = [f_dec(_, max_exp) for _ in range(1 + num1.value * 2 ** (max_exp - num1.exp),
                                               num2.value * 2 ** (max_exp - num2.exp))]
    b_list = [birthday(_) for _ in d_list]
    b_min = min(b_list)
    for d in range(len(d_list)):
        if b_list[d] == b_min:
            return d_list[d]


hole_num_dict = dict()


def calc_nimber(num):
    L_list = [calc_nimber(_) for _ in num.L]
    R_list = [calc_nimber(_) for _ in num.R]
    if len(L_list) + len(R_list) == 0:
        return 0

    if set(L_list) != set(R_list):
        return -1

    if -1 in L_list or -1 in R_list:
        return -1
    temp = 0

    while temp in L_list:
        temp += 1

    return temp


def calc_number(num):
    L_list = num.L
    R_list = num.R

    if str(num) in hole_num_dict:
        return hole_num_dict[str(num)].copy()
    L_list = [calc_number(_) for _ in L_list]
    R_list = [calc_number(_) for _ in R_list]

    if False in L_list or False in R_list:
        return False
    L_num = None
    R_num = None
    if len(L_list) == 0 and len(R_list) == 0:
        hole_num_dict[str(num)] = f_dec(0, 0)
        return f_dec(0, 0)

    if len(L_list) > 0:
        L_num = max(L_list)
    if len(R_list) > 0:
        R_num = min(R_list)
    if len(L_list) > 0 and len(R_list) > 0:
        if L_num >= R_num:
            return False
    hole_num_dict[str(num)] = between_dec(L_num, R_num)
    return hole_num_dict[str(num)].copy()


def partisan_make(l_set, r_set):
    temp = partisan()
    temp.L = l_set
    temp.R = r_set
    return partisan_add(temp, partisan())


def partisan_add(x, y):
    temp_L = []
    for x_L in x.L:
        temp_L.append(partisan_add(x_L, y))
    for y_L in y.L:
        temp_L.append(partisan_add(x, y_L))

    temp_R = []
    for x_R in x.R:
        temp_R.append(partisan_add(x_R, y))
    for y_R in y.R:
        temp_R.append(partisan_add(x, y_R))
    temp = partisan()
    temp.L = temp_L
    temp.R = temp_R
    return temp


def partisan_mul(x, y):
    temp_L = []
    temp_R = []

    for x_L in x.L:
        for y_L in y.L:
            temp_L.append(partisan_mul(x_L, y) + partisan_mul(x, y_L) - partisan_mul(x_L, y_L))
    for x_R in x.R:
        for y_R in y.R:
            temp_L.append(partisan_mul(x_R, y) + partisan_mul(x, y_R) - partisan_mul(x_R, y_R))

    for x_L in x.L:
        for y_R in y.R:
            temp_R.append(partisan_mul(x_L, y) + partisan_mul(x, y_R) - partisan_mul(x_L, y_R))
    for x_R in x.R:
        for y_L in y.L:
            temp_R.append(partisan_mul(x_R, y) + partisan_mul(x, y_L) - partisan_mul(x_R, y_L))

    return partisan_make(temp_L, temp_R).std()


class partisan:

    def __init__(self):
        self.L = []
        self.R = []
        return

    def __add__(self, other):
        return partisan_add(self, other)

    def __sub__(self, other):
        return self + other.bar()

    def bar(self):
        return partisan_make([right.bar() for right in self.R],
                             [left.bar() for left in self.L])

    def __neg__(self):
        return self.bar()

    def __rmul__(self, other):
        temp = partisan()
        for _ in range(abs(other)):
            temp = temp + (self if other > 0 else -self)
        return temp

    def __str__(self):
        temp = "{" + ", ".join([str(_) for _ in self.L]) + "|"
        temp += "" + ", ".join([str(_) for _ in self.R]) + "}"
        return temp

    def copy(self):
        return partisan_make(self.L, self.R)

    def equal(self, y):
        partisan_make(y.L, y.R)
        return self

    def judge(self):
        temp_L = [j_L.judge() for j_L in self.L]
        temp_R = [j_R.judge() for j_R in self.R]

        L_win = False
        R_win = False

        if "L" in temp_L or "P" in temp_L:
            L_win = True
        if "R" in temp_R or "P" in temp_R:
            R_win = True

        if L_win is True and R_win is True:
            return "N"
        elif L_win is True and R_win is False:
            return "L"
        elif L_win is False and R_win is True:
            return "R"
        else:
            return "P"

    def __lt__(self, other):
        return partisan_add(self, other.bar()).judge() == "R"

    def __gt__(self, other):
        return partisan_add(self, other.bar()).judge() == "L"

    def __eq__(self, other):
        return partisan_add(self, other.bar()).judge() == "P"

    def __ne__(self, other):
        return partisan_add(self, other.bar()).judge() == "N"

    def std_L(self):
        self.L = [l0.std() for l0 in self.L]

        cancel = False

        while not cancel:
            temp_L = []
            cancel = True
            for l1 in self.L:
                cancel_ = False
                temp_LL = []
                for l2 in l1.R:
                    if l2 < self or l2 == self:
                        temp_LL = temp_LL + l2.L
                        cancel = False
                        cancel_ = True
                if not cancel_:
                    temp_L.append(l1.copy())
                else:
                    temp_L = temp_L + temp_LL
            self.L = temp_L

        temp_LLL = []
        for l3 in self.L:
            temp_LLLL = []
            for l4 in self.L:
                if l3 < l4:
                    temp_LLLL.append([l4])
            if len(temp_LLLL) == 0 and l3 not in temp_LLL:
                temp_LLL.append(l3)
        self.L = temp_LLL

        return self

    def std_R(self):

        self.R = (((self.bar()).std_L()).bar()).R
        return self

    def std(self):
        self.std_L()
        self.std_R()
        return self

    def to_number(self):

        s_num = calc_number(self)
        if s_num is not False:
            return s_num
        s_num = calc_nimber(self)
        if s_num != -1:
            return f"[{s_num}]"

        temp_L = [left.to_number() for left in self.L]
        temp_R = [right.to_number() for right in self.R]

        temp = "{" + ", ".join([str(_) for _ in temp_L]) + " | "
        temp += "" + ", ".join([str(_) for _ in temp_R]) + "}"

        return temp

    def view(self, graph: Digraph):
        graph.node(str(id(self)), str(self.to_number()))
        for l_option in self.L:
            l_option.view(graph)
            graph.edge(str(id(self)), str(id(l_option)), color='blue')

        for r_option in self.R:
            r_option.view(graph)
            graph.edge(str(id(self)), str(id(r_option)), color='red')

        return graph


def inZ(z):
    if z == 0:
        return partisan()
    elif z > 0:
        return partisan_make([inZ(z - 1)], [])
    elif z < 0:
        return partisan_make([], [inZ(z + 1)])
