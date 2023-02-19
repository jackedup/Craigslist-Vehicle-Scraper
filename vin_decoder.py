from vpic import TypedClient
c = TypedClient()

class vin_decoder:
    #end goal is to build a local copy of this for faster queries
    #downloadable endpoint is a microsoft sql 2012 backup
    def decode_vin(vin):
        result = c.decode_vin(vin)
        return {"make":result.make, "model": result.model, "year": result.model_year}

