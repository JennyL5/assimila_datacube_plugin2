import os
import json
import copy
from collections import namedtuple, OrderedDict as odict

from .dq_exceptions import DQError, DBError
from .dq_db_connect import DqDbConnection
from .setup_logger import SetUpLogger
import logging
import os.path as op
from enum import Enum

class meta_lookup(Enum):
    PRODUCT = 0
    SUBPRODUCT = 1
    BOUNDS = 2
    TILE = 3


# TODO docstrings need :param xxx: :raise xxx: and :return: entries

class DQDataBaseView:
    """
    """
    # class attribute logger
    logger = None

    def __init__(self, connect_yaml=None):
        """
        Initialise the catalogue
        Set up logging and DB connection.
        :param connect_yaml: optionally provide sql connection information
        to be passed to DqDbConnection.
        :raise DQError: For any faults
        :return:        N/A
        """
        if self.logger is None:
            SetUpLogger.setup_logger(
                default_config=op.abspath(op.join(op.dirname(__file__),
                                                  "./logging_config.yml")))
            self.logger = logging.getLogger("__main__")

        searchable_prod_meta = os.path.join(os.path.dirname(__file__),
                                            "product_meta.json")
        searchable_sub_prod_meta = os.path.join(os.path.dirname(__file__),
                                                "sub_product_meta.json")

        try:
            # Load the metadata schemas for products and sub-products
            with open(searchable_prod_meta, 'r') as f:
                self.prod_meta_schema = json.load(f)
            with open(searchable_sub_prod_meta, 'r') as f:
                self.sub_prod_meta_schema = json.load(f)

        except json.JSONDecodeError as e:
            err_msg = f"Failed to initialise searchable items. Cannot " \
                      f"load json schema.\n{e}"
            self.logger.warning(err_msg)
            raise DQError(err_msg)

        try:
            # set up a connection to the DQ database
            self.db_conn = DqDbConnection(connect_yaml=connect_yaml)
            self.db_conn.connect()

        except DBError as e:
            err_msg = f'Cannot initialise database connection.\n{e}'
            self.logger.error(err_msg)
            raise DQError(err_msg)


    def search(self, query):
        """
        Search the database and return all matching records as a
        dictionary of JSON-like data.
        If query is a string, it will be treated as a list of one string item.
        If query is a list of strings, then all records where items in the
        string are present in a product or sub-product's keywords will be
        returned.
        If query is a dictionary then only records where _all_ of the
        strings match exactly will be returned. The search will be in
        metadata of product and sub-product only.
        :param query:   Can be a string or a dictionary of key:values.
        :raise DQError: For any faults
        :return:        Matching product and sub-products
        """
        try:
            # Perform the appropriate search, given the input query type
            if isinstance(query, str):
                return self._search_general([query])
            elif isinstance(query, list):
                return self._search_general(query)
            elif isinstance(query, dict):
                return self._search_specific(query)
            else:
                raise DQError('Search query must be string (for general '
                              'search) or dictionary (for field-specific '
                              'search)')

        except (DQError, Exception) as e:
            self.logger.warning(f"Failed to search.\n{e}")
            raise DQError(f"Failed to search.") from e

    def _search_general(self, query):
        """
        Search all keywords in product and sub-product tables for any matches
        in the query list.
        :param query: list of strings
        :return: dictionary with entry for each of product and sub-product,
        where each value is a list of dictionaries with keys "name" and "id".
        """
        try:
            result = {'products': [], 'sub-products': []}

            # construct query of keywords
            terms = [f"keywords like '%{item}%'" for item in query]
            where = " OR ".join(terms)

            # find in the product table
            sql = f"SELECT name, idproduct FROM public.product WHERE {where}"
            rows = self.db_conn.get(sql)
            for row in rows:
                result['products'].append(dict(zip(('name', 'id'), row)))

            # find in sub-product table
            sql = f"SELECT name, idsubproduct FROM public.subproduct WHERE {where}"
            rows = self.db_conn.get(sql)
            for row in rows:
                result['sub-products'].append(dict(zip(('name', 'id'), row)))

            return result

        except DBError as e:
            err_msg = "General search failed."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def _search_specific(self, query):
        """
        Search all metadata in product and sub-product tables for matches in
        the query dictionary. All must match for a result.
        :param query: dictionary of metadata:value pairs
        :return: dictionary with entry for each of product and sub-product,
        where each value is a list of dictionaries with keys "name" and "id".
        """
        try:
            result = {'products': [], 'sub-products': []}

            # Create the core of the query string - convert the schema dictionary
            # into a list of just its keys, and if the key is in the query,
            # assemble the sql equality check.
            terms = [f"{key} = '{query[key]}'" for key in query
                     if key in list(self.prod_meta_schema)]
            where = " and ".join(terms)

            if terms:
                # find in the product table
                sql = f"SELECT name, idproduct FROM public.product WHERE {where}"
                rows = self.db_conn.get(sql)
                for row in rows:
                    result['products'].append(dict(zip(('name', 'id'), row)))

            terms = [f"{key} = '{query[key]}'" for key in query
                     if key in list(self.sub_prod_meta_schema)]
            where = " and ".join(terms)

            if terms:
                # find in sub-product table
                sql = f"SELECT name, idsubproduct FROM public.subproduct WHERE {where}"
                rows = self.db_conn.get(sql)
                for row in rows:
                    result['sub-products'].append(dict(zip(('name', 'id'), row)))

            return result

        except DBError as e:
            err_msg = "Specific search failed."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def search_pid(self, pid):
        """
        Search specific id in both product and sub-products.
        :param pid: an id
        :return: dictionary with entry for each of product and sub-product,
        where each value is a dictionary of metadata name/value pairs.
        """
        try:
            result = {'products': {}, 'sub-products': {}}

            sql = f"SELECT * FROM public.product WHERE idproduct={int(pid)}"
            rows = self.db_conn.get(sql)

            # Turn this into a dictionary by using the schema
            result['products'] = odict(zip(list(self.prod_meta_schema),
                                           rows[0]))

            sql = f"SELECT * FROM public.subproduct WHERE idsubproduct=" \
                  f"{int(pid)}"
            rows = self.db_conn.get(sql)

            # Turn this into a dictionary by using the schema
            result['sub-products'] = odict(
                zip(list(self.sub_prod_meta_schema), rows[0]))

            return result

        except DBError as e:
            err_msg = f"SQL search failed for product {pid}."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_name(self, product_id=None, sub_product_id=None):
        """
        Find the name of a product or sub-product given its id.
        :param product_id: unique id of product
        :param sub_product_id: unique id of sub-product
        :return: name of product or sub-product
        """
        try:
            if product_id and sub_product_id:
                raise DQError('Specify either id but not both.')
            elif product_id:
                sql = f'SELECT name FROM product ' \
                      f'WHERE idproduct={int(product_id)}'
                rows = self.db_conn.get(sql)
                if rows:
                    return rows[0][0]
                else:
                    raise DBError('No rows')

            elif sub_product_id:
                sql = f'SELECT name FROM subproduct ' \
                      f'WHERE idsubproduct={int(sub_product_id)}'
                rows = self.db_conn.get(sql)
                if rows:
                    return rows[0][0]
                else:
                    raise DBError('No rows')
            else:
                raise DQError('Neither id specified.')

        except DBError as e:
            err_msg = f"SQL retrieve failed to find name.\n{e}"
            self.logger.warning(err_msg)
            raise DQError(err_msg)

    def get_id(self, product_name, sub_product_name=None):
        """
        Find the unique id of a product from its name, or of a sub-product
        from its name and its parent's name.
        :param product_name: unique name of product
        :param sub_product_name: name of sub-product, may not be unique.
        :return: id of product if arg1 provided, id of sub-product if arg1
        and arg2 are provided
        """
        try:
            if not product_name and sub_product_name:
                raise DQError('Must specify product name if requiring a '
                              'sub-product id.')
            elif product_name and sub_product_name is None:
                sql = f"SELECT idproduct FROM product " \
                      f"WHERE name ='{product_name}'"
                rows = self.db_conn.get(sql)
                if rows:
                    return rows[0][0]
                else:
                    raise DBError('No rows')

            elif product_name and sub_product_name:
                sql = f"SELECT subproduct.idsubproduct FROM subproduct " \
                      f"INNER JOIN product ON " \
                      f"  (product.idproduct = subproduct.idproduct) " \
                      f"WHERE subproduct.name ='{sub_product_name}' " \
                      f"AND product.name ='{product_name}'"

                rows = self.db_conn.get(sql)
                if rows:
                    return rows[0][0]
                else:
                    raise DBError('No rows')
            else:
                raise DQError('Neither name specified.')

        except DBError as e:
            err_msg = f"SQL retrieve failed to find id.\n{e}"
            self.logger.warning(err_msg)
            raise DQError(err_msg)

    def get_product_from_subproduct_id(self, sub_product: int):
        """
        Given the id of a sub_product, find details of the parent product
        :param sub_product: unique id of sub-product
        :return: name and id of parent product in a dictionary
        """
        try:
            sql = f"SELECT product.name, product.idproduct FROM product " \
                  f"INNER JOIN subproduct ON " \
                  f"  (subproduct.idproduct = product.idproduct) " \
                  f"WHERE subproduct.idsubproduct = {int(sub_product)}"
            row = self.db_conn.get(sql)
            if row:
                result = {'name': row[0][0], 'id': row[0][1]}
                return result
            else:
                raise DBError('No rows')

        except DBError as e:
            err_msg = f"SQL retrieve failed to find product details."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_products_from_subproduct_name(self, sub_product: str):
        """
        Given the name of a sub-product, this method finds the names of the
        possible parent products.
        :param sub_product: name of sub-product
        :return: list of product names
        """
        try:
            result = []
            # There *may* be many parents
            sql = f"SELECT product.name FROM product " \
                  f"INNER JOIN subproduct ON " \
                  f"  (subproduct.idproduct = product.idproduct) " \
                  f"WHERE subproduct.name = '{sub_product}'"
            rows = self.db_conn.get(sql)
            if rows:
                # iterate through rows and collect up first/only element of tuple
                for row in rows:
                    result.append(row[0])
                return result
            else:
                raise DBError('No rows')

        except DBError as e:
            err_msg = f"SQL retrieve failed to find products."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_subproducts_from_product_name(self, product: str):
        """
        Given the name of a product, this method finds the names of all its
        sub-products.
        :param product:  name of product
        :return: list of sub-product names
        """
        try:
            result = []
            # There may be many children
            sql = f"SELECT subproduct.name FROM subproduct " \
                  f"INNER JOIN product ON " \
                  f"  (product.idproduct = subproduct.idproduct) " \
                  f"WHERE product.name = '{product}'"
            rows = self.db_conn.get(sql)

            if rows:
                # iterate through rows and collect up first/only
                # element of tuple
                for row in rows:
                    result.append(row[0])
                return result
            else:
                raise DBError('No rows')

        except DBError as e:
            err_msg = f"SQL retrieve failed to find subproducts."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_metadata(self, meta_get_list):
        """
        Get the metadata for each of the product/sub-product pairs provided in
        the list.
        The metadata consists of the fields in each table. No dates are
        currently retrieved.
        :param meta_get_list: list of prod/sub-prod tuples optionally with a
        bounds sub-tuple.
        :return: metadata in a list of lists of dataframes - each sub-list
        has one df each for the product and subproduct.
        :raise DQError: if the argument is an empty list,
        or product/sub-product is not found.
        """
        try:
            # check to see if we've got anything to process...
            dummy = meta_get_list[0]

            # prepare return data
            results = []
            for details in meta_get_list:
                result = []
                sql = f"SELECT * FROM product " \
                      f"WHERE name = '{details[meta_lookup.PRODUCT.value]}'"

                df = self.db_conn.get_df(sql)
                if not df.empty:
                    result.append(df)

                else:
                    raise DBError(f'No rows for the given product: '
                                  f'{details[meta_lookup.PRODUCT.value]}.')

                subproduct_id = self.get_id(product_name=details[meta_lookup.PRODUCT.value],
                                            sub_product_name=details[
                                                meta_lookup.SUBPRODUCT.value])

                # # Ascertain whether any data has been written yet. How many
                # # dates do we have for this subproduct in relfilebanddate?
                # dates_sql = "SELECT COUNT(*) FROM subproduct " \
                #       "INNER JOIN file ON " \
                #       "  (subproduct.idsubproduct = file.idsubproduct) " \
                #       "INNER JOIN relfilebanddate ON  " \
                #       "  (file.idfile = relfilebanddate.idfile) "\
                #       f"WHERE file.idsubproduct = '{subproduct_id}' "
                #
                # num_dates = self.db_conn.get(dates_sql)[0][0]

                # Try to get the full metadata, if this fails, fetch the
                # short metadata
                df = self.get_long_metadata(subproduct_id, details)

                if df.empty:
                    df = self.get_short_metadata(subproduct_id, details)

                try:
                    result.append(df)
                    results.append(result.copy())
                except:
                    raise DBError(f'No rows for the given sub-product:'
                                  f'{details[meta_lookup.SUBPRODUCT.value]}')

                # # # If there are dates recorded, get the full dataframe,
                # # # otherwise just extract the core information about product
                # # # and subproduct.
                # # # Todo: this can probably be divided up more nicely
                # # if num_dates:
                # #     df = self.get_long_metadata(subproduct_id, details)
                # # else:
                # #     df = self.get_short_metadata(subproduct_id, details)
                #
                # if not df.empty:
                #
                #
                # else:
                #     raise DBError(f'No rows for the given sub-product:'
                #                   f'{details[meta_lookup.SUBPRODUCT.value]}')

                return results

                # todo: put in if statment here to filter where files not yet
                #  written

        except IndexError as e:
            # we were passed an empty list
            err_msg = 'Cannot retrieve metadata; no product/sub-product ' \
                      'pairs provided.'
            self.logger.error(err_msg)
            raise DQError(err_msg)

        except DBError as e:
            err_msg = f"SQL retrieve failed to find product/subproducts."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_short_metadata(self, subproduct_id,  details):
        """
        Get the 'short' metadata metadata for a subproduct. Short metadata is a
        dataframe containing the following columns of data about a subproduct:
        - id
        - name
        - long name
        - description
        - units
        - minimum value
        - maximum value
        - keywords
        - link
        - scale factor
        - offset
        - fill value
        - parent product id
        - tiles name
        ...and a row for each available tile
        :param details: list of
        :return: dataframe result of the sql query
        :raise DQError: if the argument is an empty list,
        or product/sub-product is not found.
        """

        try:

            sql = "SELECT subproduct.idsubproduct, subproduct.name, " \
                  "  longname, description, units, minvalue, maxvalue, " \
                  "  keywords, link, datascalefactor, dataoffset, " \
                  "  datafillvalue, idproduct,  frequency, " \
                  "  tile.name as tilename FROM subproduct " \
                  "INNER JOIN relsubproducttile ON " \
                  "  (relsubproducttile.idsubproduct=" \
                  "  subproduct.idsubproduct)" \
                  "INNER JOIN tile ON " \
                  "  (relsubproducttile.idtile = tile.idtile) " \
                  "INNER JOIN boundingbox ON " \
                  "  (tile.idboundingbox = boundingbox.idboundingbox)" \
                  f"WHERE subproduct.idsubproduct = '{subproduct_id}' "

            if len(details) == meta_lookup.BOUNDS.value + 1 and \
                details[meta_lookup.BOUNDS.value] is not None:

                Bounds = namedtuple('Bounds', 'north south east west')

                # Add bounds to named tuple instance
                bounds = Bounds(**details[meta_lookup.BOUNDS.value])

                sql += "AND ST_Intersects(" \
                      "ST_GeomFromText(ST_AsEWKT(boundingbox.geography),4326)," \
                      f"ST_MakeEnvelope({bounds.west}, {bounds.south}, " \
                      f"{bounds.east}, {bounds.north}, 4326))"

            df = self.db_conn.get_df(sql)

            return df

        except DBError as e:
            err_msg = f"SQL retrieve failed to find product/subproducts."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e


    def get_long_metadata(self, subproduct_id,  details):
        """
        Get the 'long' metadata metadata for a subproduct. Long metadata is a
        dataframe containing the following columns of data about a subproduct:
        - id
        - name
        - long name
        - description
        - units
        - minimum value
        - maximum value
        - keywords
        - link
        - scale factor
        - offset
        - fill value
        - parent product id
        - all dates available
        - all tiles available
        and rows for each available date and tile combination
        :param details: list of
        :return: dataframe result of the sql query
        :raise DQError: if the argument is an empty list,
        or product/sub-product is not found.
        """

        try:

            sql = "SELECT subproduct.idsubproduct, subproduct.name, " \
                  "  longname, description, units, minvalue, maxvalue, " \
                  "  keywords, link, datascalefactor, dataoffset, " \
                  "  datafillvalue, idproduct, frequency, " \
                  "  relfilebanddate.datetime, relfilebanddate.gold, " \
                  "  tile.name as tilename FROM subproduct " \
                  "INNER JOIN file ON " \
                  "  (subproduct.idsubproduct = file.idsubproduct) " \
                  "INNER JOIN relfilebanddate ON  " \
                  "  (file.idfile = relfilebanddate.idfile) " \
                  "INNER JOIN reltilefile ON " \
                  "  (reltilefile.idfile=file.idfile)" \
                  "INNER JOIN tile ON " \
                  "  (reltilefile.idtile = tile.idtile) " \
                  "INNER JOIN boundingbox ON " \
                  "  (tile.idboundingbox = boundingbox.idboundingbox)" \
                  f"WHERE file.idsubproduct = '{subproduct_id}' "

            if len(details) == meta_lookup.BOUNDS.value + 1 and \
                details[meta_lookup.BOUNDS.value] is not None:

                # If a user has requested data within particular bounds,
                # we return metadata on the tiles of this product which
                # intersect those bounds

                Bounds = namedtuple('Bounds', 'north south east west')

                # Add bounds to named tuple instance
                bounds = Bounds(**details[meta_lookup.BOUNDS.value])

                sql += "AND ST_Intersects(" \
                      "ST_GeomFromText(ST_AsEWKT(boundingbox.geography),4326)," \
                      f"ST_MakeEnvelope({bounds.west}, {bounds.south}, " \
                      f"{bounds.east}, {bounds.north}, 4326))"

            elif len(details) == meta_lookup.TILE.value + 1 and \
                details[meta_lookup.TILE.value] is not None:

                # If a user has requested data for a particular tile,
                # we return metadata on the tiles of this product which
                # intersect that tile.

                # Get WKT for the tile
                tile_poly_wkt = self.get_wkt_from_tilename(
                    details[meta_lookup.TILE.value])

                # Use this polygon to find the intersection
                sql += "AND ST_Intersects(" \
                      "ST_GeomFromText(ST_AsEWKT(boundingbox.geography),4326)," \
                      f"ST_GeomFromText('{tile_poly_wkt}', 4326))"

            df = self.db_conn.get_df(sql)

            return df

        except DBError as e:
            err_msg = f"SQL retrieve failed to find product/subproducts."
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def check_product_exists(self, product_name):
        """
        Method to check that the product found in the input x-array
        dataset contains a valid product found in the data cube.
        :return: True or false depending on whether the product
                 exists within the data cube.
        """

        # Define the command for the search
        search_products = \
            "select product.name from " \
            f"product WHERE product.name = '{product_name}'"

        try:
            result = self.db_conn.get_df(search_products)

            # If returned data frame is empty, product does not exist.
            # TODO: <re-assess if logging or raise should be used. Logging
            # does not stop the flow of archiver whereas raise would...>
            # JPL: always raise exceptions if things fail otherwise the caller cannot know.
            if result.empty:
                err_msg = (f"Product: {product_name} not found. Please register first or check "
                           f"input x-array.")
                self.logger.warning(err_msg)
                raise DQError(err_msg)

            else:
                return True

        except DBError as e:
            err_msg = f'Search for product: {product_name} failed.'
            self.logger.error(err_msg)
            raise DQError(err_msg) from e

    def check_subproduct_exists(self, product_name, subproduct_name):
        """
        Method to check that the subproduct found in the input x-array
        dataset contains a valid subproduct found in the data cube.
        :return: True or false depending on whether the subproduct
                 exists within the data cube.
        """

        # Define the command for the search
        search_subproducts = \
            "SELECT subproduct.name, subproduct.idsubproduct from subproduct " \
            "INNER JOIN product ON (subproduct.idproduct = product.idproduct) " \
            f"WHERE product.name = '{product_name}' " \
            f"AND subproduct.name = '{subproduct_name}'"

        try:

            result = self.db_conn.get_df(search_subproducts)

            # Return true if subproduct name is within valid subproducts
            # TODO: <re-assess if logging or raise should be used. Logging
            # does not stop the flow of archiver whereas raise would...>
            if result.empty:
                err_msg = (f"Subproduct: {subproduct_name} not "
                                    f"found. Please register first or check "
                                    f"input x-array.")
                self.logger.warning(err_msg)
                raise DQError(err_msg)
            else:
                return True

        except DBError as e:
            err_msg = f'Search for product: {subproduct_name} failed.'
            self.logger.error(err_msg)
            raise DQError(err_msg) from e

    def get_scale_offset_fill_for_subproduct(self, subproduct_id):
        """
        Set the scale, offset and fill attributes from the subproduct's
        record.
        :return: DB return of scale factor, offset and data fill value.
        """
        # Define the command for the search
        search_data_factors = f"SELECT datascalefactor, dataoffset, " \
                              f"  datafillvalue " \
                              f"FROM public.subproduct " \
                              f"WHERE idsubproduct = {subproduct_id}"

        # Send the search to the database - result is list of tuples;
        # we want the items in the first (and only) row
        try:

            result = self.db_conn.get(search_data_factors)
            return result

        except DBError as e:
            err_msg = f'Unable to read datascalefactor, dataoffset,' \
                      f'datafillvalue from subproduct: {subproduct_id}'
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_min_max_value_for_subproduct(self, subproduct_id):
        """
        Set the maximum and minimum value attributes from the s
        subproduct's record.
        :return: DB return of scale factor, offset and data fill value.
        """
        # Define the command for the search
        search_data_factors = f"SELECT minvalue, maxvalue " \
                              f"FROM public.subproduct " \
                              f"WHERE idsubproduct = {subproduct_id}"

        # Send the search to the database - result is list of tuples;
        # we want the items in the first (and only) row
        try:

            result = self.db_conn.get(search_data_factors)
            return result

        except DBError as e:
            err_msg = f'Unable to read minvalue, maxvalue ' \
                      f'from subproduct: {subproduct_id}'
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_tilename_from_wkt(self, wkt, projection):
        """
        Find the tile that overlaps the geometry (in native coordinate
        system) created from the  well known text. Set the tile
        attribute
        :param wkt:           WKT to create polygon in product native
                              coordinates
        :param projection:
        :return: Return matching tile
        """

        # Search tile name by finding the bounding box in EPSG:4326
        # that matches (performing a snap to a grid of 0.00001 res)
        # the WKT in product's native CRS, e.g. Sinusoidal

        sql_tile = (
            f"SELECT tile.name "
            f"FROM public.tile, public.boundingbox "
            f"WHERE "
            f"  boundingbox.idboundingbox = tile.idboundingbox AND "
            f"  ST_Equals("
            f"    ST_SnapToGrid(ST_AsEWKT(boundingbox.geography), 0.00001),"
            f"  ST_SnapToGrid(ST_AsEWKT(ST_Transform("
            f"    ST_GeomFromText('{wkt}','{projection}'), 4326)), "
            f"    0.00001));")

        # Send the search to the database
        try:
            return self.db_conn.get(sql_tile)[0][0]

        except (DBError, IndexError) as e:
            err_msg = f'Unable to get tile name from wkt: {wkt}'
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_wkt_from_tilename(self, tilename):
        """
        Extract the Well Known Text for this tile
        :param wkt:           WKT to create polygon in product native
                              coordinates
        :param projection:
        :return: Return matching tile
        """

        sql_tile = "SELECT ST_AsText(geography) FROM " \
                   "boundingbox INNER JOIN tile ON (" \
                   "boundingbox.idboundingbox = " \
                   "tile.idboundingbox) WHERE tile.name = " \
                   f"'{tilename}'"

        # Send the search to the database
        try:
            return self.db_conn.get(sql_tile)[0][0]

        except (DBError, IndexError) as e:
            err_msg = f'Unable to get wkt name from tile name: {tilename}'
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_existing_data_from_database(self, months, years,
                                        subproduct_id, dq_tile):
        """
        :param months:
        :param years:
        :param subproduct_id:
        :param dq_tile:
        :return:
        """

        months_query = ''
        for month in months:
            months_query = (f"{months_query} EXTRACT(MONTH FROM "
                            f"relfilebanddate.datetime) = {month} OR")

        years_query = ''
        for year in years:
            years_query = (f"{years_query} EXTRACT(YEAR FROM "
                           f"relfilebanddate.datetime) = {year} OR")

        years_months_query = f"(({years_query[1:-3]}) AND " \
                             f"({months_query[1:-3]}));"

        search_bands_dates = \
            "SELECT file.filename, relfilebanddate.band," \
            "  relfilebanddate.datetime, subproduct.datascalefactor," \
            "  subproduct.dataoffset, subproduct.datafillvalue " \
            "FROM " \
            "  public.product, public.subproduct, " \
            "  public.file, " \
            "  public.relsubproducttile, public.tile, " \
            "  public.reltilefile, public.relfilebanddate " \
            "WHERE " \
            "  product.idproduct = subproduct.idproduct AND" \
            "  subproduct.idsubproduct = relsubproducttile.idsubproduct AND" \
            "  file.idfile = relfilebanddate.idfile AND" \
            "  relsubproducttile.idtile = tile.idtile AND" \
            "  tile.idtile = reltilefile.idtile AND" \
            "  reltilefile.idfile = file.idfile AND" \
            "  subproduct.idsubproduct = file.idsubproduct AND" \
            f" tile.name = '{dq_tile}' AND" \
            f" subproduct.idsubproduct = '{subproduct_id}' AND" \
            f" {years_months_query}"

        try:
            return self.db_conn.get_df(search_bands_dates)

        except (DBError, IndexError) as e:
            err_msg = f'Unable to get existing data for sub-product: {subproduct_id}, tile: {dq_tile}.'
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    def get_projection_for_product(self, product):
        """
        Get projection from a product name.
        :param product:
        :return: db projection
        """

        search_srid = (
            f"SELECT spatial_ref_sys.srid "
            f"FROM public.product, public.spatial_ref_sys "
            f"WHERE "
            f"product.srid = spatial_ref_sys.srid AND "
            f"product.name = '{product}';")

        # Send the search to the database
        try:

            return self.db_conn.get(search_srid)[0][0]

        except (DBError, IndexError) as e:
            err_msg = f'Unable to get projection for {product}'
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

    # TODO move these functions to utils - they may be useful in future
    # @staticmethod
    # def _format_for_database(md):
    #     """
    #     Convert tricky data types for the catalogue
    #
    #     :param md:
    #
    #     :return:
    #     """
    #     md_copy = copy.deepcopy(md)
    #     # Replace lists. This applies to geo-transform and dates.
    #     for entry in md_copy:
    #         # Handle the lists
    #         if isinstance(md_copy[entry], list):
    #
    #             if entry == 'geo_transform':
    #                 md_copy[entry] = str(md_copy[entry])
    #
    #             elif entry == 'dates':
    #                 list_of_strings = [str(d) for d in md_copy[entry]]
    #                 string_of_list = str(list_of_strings).replace('\'', '\"')
    #                 md_copy[entry] = string_of_list
    #
    #         # Handle the dates
    #         if isinstance(md_copy[entry], np.datetime64):
    #             date_as_string = str(md_copy[entry])
    #             md_copy[entry] = date_as_string
    #
    #     return md_copy
    #
    # @staticmethod
    # def _format_for_dq(md):
    #     """
    #     Convert fields back into a list (inverse of
    #     _format_for_database) for use back in the main body of the
    #     data cube.
    #
    #     :param md:
    #
    #     :return: TODO
    #     """
    #     md_copy = copy.deepcopy(md)
    #
    #     # geo_transform is a list of floats.
    #     if 'geo_transform' in \
    #             md_copy and isinstance(md_copy['geo_transform'], str):
    #
    #         list_of_strings = md_copy['geo_transform'][1:-1].split(",")
    #         md_copy['geo_transform'] = [float(n) for n in list_of_strings]
    #
    #     # Dates is a list of datetime strings, which can have line breaks
    #     if 'dates' in md_copy and isinstance(md_copy['dates'], str):
    #
    #         list_of_strings = md_copy['dates'][1:-1].replace('\"', '').split(", ")
    #         list_of_np64s = [np.datetime64(s, 'm') for s in list_of_strings]
    #         md_copy['dates'] = list_of_np64s
    #
    #     # Last gold is stored as a string. Convert back to np 64.
    #     if 'last_gold' in md and isinstance(md_copy['last_gold'], str):
    #         md_copy['last_gold'] = np.datetime64(md_copy['last_gold'])
    #
    #     return md_copy

class BespokeSearch(DQDataBaseView):
    """
    Generic catch-all location for adding in new searches as required
    """

    def get_search(self, search_name, params):
        """
        :param search_name: This must match the function name
        :param params: This is passed to the function
        :return:
        """

        # Extract the function from the string
        func = getattr(self, search_name)

        # Run the method passed and pass results back
        return func(params)


    def get_tables(self, table_name):
        """
        Extract all entries in the table specified
        :param table_name:
        :return:
        """

        sql_command = f"select * from {table_name}"

        # Send the search to the database
        try:
            result = self.db_conn.get_df(sql_command)
            return result

        except (DBError, IndexError) as e:
            err_msg = f'Unable to get wkt name from table: {table_name}'
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e

        except Exception as e:
            err_msg = e
            self.logger.warning(err_msg)
            raise DQError(err_msg) from e