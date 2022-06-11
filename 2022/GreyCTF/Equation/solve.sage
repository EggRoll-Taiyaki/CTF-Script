v1 = 6561821624691895712873377320063570390939946639950635657527777521426768466359662578427758969698096016398495828220393137128357364447572051249538433588995498109880402036738005670285022506692856341252251274655224436746803335217986355992318039808507702082316654369455481303417210113572142828110728548334885189082445291316883426955606971188107523623884530298462454231862166009036435034774889739219596825015869438262395817426235839741851623674273735589636463917543863676226839118150365571855933
v2 = 168725889275386139859700168943249101327257707329805276301218500736697949839905039567802183739628415354469703740912207864678244970740311284556651190183619972501596417428866492657881943832362353527907371181900970981198570814739390259973631366272137756472209930619950549930165174231791691947733834860756308354192163106517240627845889335379340460495043

P.<m1, m2> = PolynomialRing(ZZ, 2)
f = 13 * m2 ** 2 + m1 * m2 + 5 * m1 ** 7 - v1
g = 7 * m2 ** 3 + m1 ** 5 - v2

h = f.resultant(g)
i = h.univariate_polynomial()
_m2 = i.roots()[0][0]
j = g.subs({m2: _m2}).univariate_polynomial()
_m1 = j.roots()[0][0]

from Crypto.Util.number import *

flag = long_to_bytes(_m1) + long_to_bytes(_m2)
print(flag)
