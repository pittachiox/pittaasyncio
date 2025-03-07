import asyncio
import random

class Restaurant:
    def __init__(self, num_tables):
        self.tables = asyncio.Semaphore(num_tables)  # ควบคุมจำนวนโต๊ะ
        self.waiting_customers = asyncio.Queue()  # คิวลูกค้าที่รอโต๊ะ

    async def seat_customer(self, customer_id):
        """จัดที่นั่งให้ลูกค้า"""
        await self.tables.acquire()
        print(f"🪑 ลูกค้า {customer_id} ได้โต๊ะ")
        await self.take_order(customer_id)

    

async def customer_task(customer_id, restaurant):
    """จำลองลูกค้าที่เข้ามาในร้าน"""
    print(f"🚶‍♂ ลูกค้า {customer_id} เข้าร้าน")
    await restaurant.waiting_customers.put(customer_id)
    await restaurant.seat_customer(customer_id)

async def main():
    num_tables = 3  # จำนวนโต๊ะในร้าน
    restaurant = Restaurant(num_tables)
    customers = [customer_task(i, restaurant) for i in range(1, 8)]  # มีลูกค้า 7 คน
    
    await asyncio.gather(*customers)
    await restaurant.waiting_customers.join()

if __name__ == "__main__":
    asyncio.run(main())
