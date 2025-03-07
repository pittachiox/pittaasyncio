import asyncio
import random

class Restaurant:
    def __init__(self, num_tables):
        self.tables = asyncio.Semaphore(num_tables)  # ควบคุมจำนวนโต๊ะ
        self.waiting_customers = asyncio.Queue()  # คิวลูกค้าที่รอโต๊ะ

    



async def main():
    num_tables = 3  # จำนวนโต๊ะในร้าน
    restaurant = Restaurant(num_tables)
    customers = [customer_task(i, restaurant) for i in range(1, 8)]  # มีลูกค้า 7 คน
    
    await asyncio.gather(*customers)
    await restaurant.waiting_customers.join()

if __name__ == "__main__":
    asyncio.run(main())
