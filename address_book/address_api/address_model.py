from geopy.distance import geodesic
from utils import get_logger, get_db_connection
from address_api.address_schema import Address

class AddressModel:
    def __init__(self) -> None:
        """
        Initialize AddressModel class with logger and database connection.
        """
        self.app_log = get_logger("address_book")
        self.conn = get_db_connection()

    async def add_address(self, address):
        """
        Add a new address to the database.

        Args:
            address: AddressCreate schema object containing address details.

        Returns:
            dict: Dictionary indicating the status of the operation.
        """
        try:
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
        """
        Get address details by address ID.

        Args:
            address_id: ID of the address to retrieve.

        Returns:
            bool: True if address exists, False otherwise.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''Select * from addresses_book where address_id = ?''', (address_id,))
            address_row = cursor.fetchone()
            if address_row:
                return True
        except Exception as err:
            self.app_log.exception(err)
            raise "Error in Checking"

    async def update_address(self, address):
        """
        Update an existing address in the database.

        Args:
            address: AddressUpdate schema object containing updated address details.

        Returns:
            dict: Dictionary indicating the status of the operation.
        """
        try:
            cursor = self.conn.cursor()
            self.app_log.info("Running Update Query")
            address_data = address.dict(exclude_unset=True)
            address_id = address_data.pop('address_id')
            if not address_data:
                return {"error": "No Field Provided to update Address"}
            update_query = f'''UPDATE addresses_book SET {", ".join([f"{column} = ?" for column in address_data.keys()])} WHERE address_id = ?'''
            cursor.execute(update_query, (*address_data.values(), address_id))
            self.app_log.info(f'Address details updated for {address_id} address id')
            self.conn.commit()
            if cursor.rowcount == 0:
                print("No row updated")
            return {"Status": "Address Updated Successfully"}
        except Exception as err:
            cursor.close()
            self.app_log.exception(err)
            return {"error": "Error in Updating Address"}
    
    async def delete_address(self,address_id):
        """
        Delete an address from the database by address ID.

        Args:
            address_id: ID of the address to delete.

        Returns:
            dict: Dictionary indicating the status of the operation.
        """
        try:
            self.app_log.info('Running Delete Address Query')
            cursor = self.conn.cursor()
            cursor.execute('''Delete from addresses_book where address_id= ?''', (address_id,))
            self.conn.commit()
            return {"status": "Deleted Address Successfully"}
        except Exception as err:
            self.app_log.exception(err)
            raise {"error": "Error in Deleting Address"}

    async def get_address_by_distance(self, address):
        """
        Retrieve addresses within a given distance from a location.

        Args:
            address: AddressFetch schema object containing location coordinates and distance.

        Returns:
            List[Address]: List of Address schema objects within the given distance.
        """
        try:
            self.app_log.info('Fetching all the address for given values')
            cursor = self.conn.cursor()
            cursor.execute('''SELECT * FROM addresses_book''')
            output_address = []
            user_location = (address.latitude, address.longitude)
            for address_data in cursor.fetchall():
                address_response = Address(address_id=address_data[0], street=address_data[1], city=address_data[2], state=address_data[3], country=address_data[4], latitude=address_data[5], longitude=address_data[6])
                address_location = (address.latitude, address.longitude)
                distance_between = geodesic(user_location, address_location).kilometers
                if distance_between <= address.distance:
                    output_address.append(address_response)
            cursor.close()  # Close the cursor after fetching data
            return output_address
        except Exception as err:
            self.app_log.info(err)
            return {"error": "Error Fetching Data"}
