from geopy.distance import geodesic

from utils import get_logger, get_db_connection

class AddressModel:
    def __init__(self) -> None:
        self.app_log = get_logger("address_book.log")
        self.conn = get_db_connection()

    async def add_address(self, address):
        try:
            breakpoint()
            self.app_log.info("Executing add address query")
            cursor = self.conn.cursor()
            cursor.execute('''Insert into addresses_book(street, city, state, country, latitude, longitude)
                            Values(?,?,?,?,?,?)''', (address.street, address.city, address.state, address.country, address.latitude, address.longitude))
            self.conn.commit()
            cursor.close()
            return {"Status": "Address Added Successfully"}
        except Exception as err:
            cursor.close()
            self.app_log.error(err)
            return {"error": "Error in Adding Address"}
    
    async def get_address(self, address_id):
        try:
            breakpoint()
            cursor = self.conn.cursor()
            cursor.execute('''Select * from addresses_book where address_id = ?''', (address_id,))
            address_row = cursor.fetchone()
            if address_row:
                return True
        except Exception as err:
            self.app_log.exception(err)
            raise "Error in Checking"

    async def update_address(self, address):
        try:
            self.app_log("Running Update Query")
            address_data = address.dict(exclude_unset=True)
            address_id = address_data.pop('address_id')
            if not address_data:
                return {"error": "No Field Provided to update Address"}
            update_query = f'''UPDATE addresses SET {", ".join([f"{column} = ?" for column in address_data.keys()])} WHERE id = ?'''
            cursor = self.conn.cursor()
            cursor.execute(update_query, (*address_data.values(), address_id))
            self.app_log.info(f'Address details updated for {address_id} address id')
            return {"Status": "Address Updated Successfully"}
        except Exception as err:
            cursor.close()
            self.app_log.exception(err)
            return {"error": "Error in Updating Address"}
    
    async def delete_address(self,address_id):
        try:
            self.app_log.info('Running Delete Address Query')
            cursor = self.conn.commit()
            cursor.execute('''Delete from addresses_book where address_id= ?''', (address_id))
            self.conn.commit()
            return {"status": "Deleted Address Successfully"}
        except Exception as err:
            self.app_log.exception(err)
            raise {"error": "Error in Deleting Address"}
