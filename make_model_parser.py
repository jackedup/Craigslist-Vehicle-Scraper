import pandas as pd
from vin_decoder import vin_decoder
class make_model_parser:
    def parse_csv():
        df = pd.read_csv("cars.csv")
        vindf = df.loc[df["VIN"].notnull()]
        make_model_year_df = vindf.apply(lambda row: vin_decoder.decode_vin(row['VIN']), axis=1,result_type='expand')
        vindf = pd.concat([vindf, make_model_year_df],axis="columns")
        vindf = vindf[vindf["make"] != "INTERNATIONAL"]
        vindf = vindf[vindf["make"] != "HINO"]
        vindf = vindf[vindf["make"] != "KENWORTH"]
        generation_classifier.generation_classifier(vindf)
        # print(vindf)
        # novindf = df.loc[df["VIN"].isnull()]
        # print(len(vindf.index))
        # print(len(novindf.index))

generation_csv = pd.read_csv("generation.csv")
class generation_classifier:
    def gen_finder(make,model,year):
        try:#TODO: get better checking of input strings.
            int(year)
        except:
            print(f"year is not correct for {make}, {model}: {year}")
            return {"generation": "NO_MATCH"}
        gen = generation_csv.loc[(generation_csv["make"] == make) & (generation_csv["model"] == model) & (generation_csv["year_begin"] <= int(year)) & (generation_csv["year_end"] >= int(year)) ]
        if not gen.empty:
            return {"generation": str(gen["generation"].to_list()[0])} #little messy, probably pretty resource heavy since it runs for every row with apply but couldnt figure out how to get just the number, and not the index as well.
        else:
            return {"generation": "NO_MATCH"}
    def generation_classifier(vindf):
        generation_df = vindf.apply(lambda row: generation_classifier.gen_finder(row['make'],row["model"],row["year"]), axis=1,result_type='expand')
        vindf = pd.concat([vindf, generation_df], axis="columns", ignore_index=True).sort_values("price").sort_values("generation")
        print(vindf)
        vindf.to_csv("./generationdf.csv")



if __name__ == "__main__":
    make_model_parser.parse_csv()
