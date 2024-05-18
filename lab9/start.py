import os
import time

start_time = time.time()
os.system('Python -m unittest tests.AuthorizationTest')
os.system('Python -m unittest tests.FindProductTest')
os.system('Python -m unittest tests.AddProductToCart')
os.system('Python -m unittest tests.MakingOrderTest')

print(time.time() - start_time)