import asyncio
import random

class Restaurant:
    def __init__(self, num_tables):
        self.tables = asyncio.Semaphore(num_tables)  
        self.waiting_customers = asyncio.Queue()  

    async def seat_customer(self, customer_id):
        """จัดที่นั่งให้ลูกค้า"""
        await self.tables.acquire()  
        print(f"🪑 ลูกค้า {customer_id} ได้โต๊ะ")
        await self.take_order(customer_id)

    async def take_order(self, customer_id):
        """รับออเดอร์จากลูกค้า"""
        await asyncio.sleep(random.uniform(1, 3))
        print(f"📋 หุ่นยนต์รับออเดอร์จากลูกค้า {customer_id}")
        await self.prepare_food(customer_id)

    async def prepare_food(self, customer_id):
        """ทำอาหาร"""
        await asyncio.sleep(random.uniform(3, 6))
        print(f"🔥 อาหารของลูกค้า {customer_id} พร้อมเสิร์ฟ")
        await self.serve_food(customer_id)

    async def serve_food(self, customer_id):
        """เสิร์ฟอาหาร"""
        await asyncio.sleep(random.uniform(1, 2))
        print(f"🍽️ ลูกค้า {customer_id} ได้รับอาหารแล้ว")
        await self.customer_leaves(customer_id)

    async def customer_leaves(self, customer_id):
        """ลูกค้ากินเสร็จและออกจากร้าน"""
        await asyncio.sleep(random.uniform(2, 4))
        print(f"💰 ลูกค้า {customer_id} จ่ายเงินและออกจากร้าน")
        self.tables.release()  
        await self.waiting_customers.get()  
        self.waiting_customers.task_done()  

async def customer_task(customer_id, restaurant):
    """จำลองลูกค้าที่เข้ามาในร้าน"""
    print(f"🚶‍♂ ลูกค้า {customer_id} เข้าร้าน")
    await restaurant.waiting_customers.put(customer_id)  
    await restaurant.seat_customer(customer_id)

async def main():
    num_tables = 3  
    restaurant = Restaurant(num_tables)
    customers = [customer_task(i, restaurant) for i in range(1, 8)]  
    
    await asyncio.gather(*customers)  
    await restaurant.waiting_customers.join()  

if __name__ == "__main__":
    asyncio.run(main())
