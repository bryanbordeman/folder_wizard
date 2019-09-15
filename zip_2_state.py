'''==========================================
Title:  zip_2_state.py
Author:  Bryan Bordeman
Start Date:  062219
Updated:  072019 (Added NYC Boroughs)
Version:  support script
Notes: Added NYC Boroughs

;=========================================='''

def main():
    '''for testing only'''
    while True:

        zip_var = int(input('Enter Zip Code: '))
        print(find_state(zip_var))
        if zip_var == 0: # break loop
            return False

zip_code_list = [['Alaska', 'AK', 99501, 99950],
    ['Alabama', 'AL',  35004, 36925],
    ['Arkansas', 'AR', 71601, 72959],
    ['Arkansas', 'AR', 75502, 75502],
    ['Arizona', 'AZ', 85001, 86556],
    ['California', 'CA', 90001, 96162],
    ['Colorado' , 'CO', 80001, 81658],
    ['Connecticut', 'CT', 6001, 6389],
    ['Connecticut', 'CT', 6401, 6928],
    ['Dist of Columbia', 'DC', 20001, 20039],
    ['Dist of Columbia', 'DC', 20042, 20599],
    ['Dist of Columbia', 'DC', 20799, 20799],
    ['Delaware', 'DE', 19701, 19980],
    ['Florida', 'FL', 32004, 34997],
    ['Georgia', 'GA', 30001, 31999],
    ['Georga', 'GA', 39901, 39901],
    ['Hawaii', 'HI', 96701, 96898],
    ['Iowa', 'IA',  50001, 52809],
    ['Iowa', 'IA', 68119, 68120],
    ['Idaho', 'ID',  83201, 83876],
    ['Illinois', 'IL', 60001, 62999],
    ['Indiana', 'IN', 46001, 47997],
    ['Kansas', 'KS', 66002, 67954],
    ['Kentucky', 'KY', 40003, 42788],
    ['Louisiana', 'LA', 70001, 71232],
    ['Louisiana', 'LA', 71234, 71497],
    ['Massachusetts', 'MA', 1001, 2791],
    ['Massachusetts', 'MA', 5501, 5544],
    ['Maryland', 'MD', 20331, 20331],
    ['Maryland', 'MD', 20335, 20797],
    ['Maryland', 'MD', 20812, 21930],
    ['Maine', 'ME', 3901, 4992],
    ['Michigan', 'MI', 48001, 49971],
    ['Minnesota', 'MN', 55001, 56763],
    ['Missouri', 'MO', 63001, 65899],
    ['Mississippi', 'MS', 38601, 39776],
    ['Mississippi', 'MS', 71233, 71233],
    ['Montana', 'MT', 59001, 59937],
    ['North Carolina', 'NC', 27006, 28909],
    ['North Dakota', 'ND', 58001, 58856],
    ['Nebraska', 'NE', 68001, 68118],
    ['Nebraska', 'NE', 68122, 69367],
    ['New Hampshire', 'NH', 3031, 3897],
    ['New Jersey', 'NJ', 7001, 8989],
    ['New Mexico', 'NM', 87001, 88441],
    ['Nevada', 'NV', 88901, 89883],
    ['New York', 'NY', 6390, 6390],
    ['New York', 'NY', 11698, 14975],
    ['Manhattan', 'NY', 10001, 10280],
    ['Staten Island', 'NY', 10301, 10314],
    ['Bronx', 'NY', 10451, 10475],
    ['Brooklyn', 'NY', 11201, 11239],
    ['Queens', 'NY', 11004, 11005],
    ['Queens', 'NY', 11101, 11106],
    ['Queens', 'NY', 11354, 11378],
    ['Queens', 'NY', 11411, 11436],
    ['Queens', 'NY', 11691, 11697],
    ['Ohio', 'OH', 43001, 45999],
    ['Oklahoma', 'OK', 73001, 73199],
    ['Oklahoma', 'OK', 73401, 74966],
    ['Oregon', 'OR', 97001, 97920],
    ['Pennsylvania', 'PA', 15001, 19640],
    ['Rhode Island', 'RI', 2801, 2940],
    ['South Carolina', 'SC', 29001, 29948],
    ['South Dakota', 'SD', 57001, 57799],
    ['Tennessee', 'TN', 37010, 38589],
    ['Texas', 'TX', 73301, 73301],
    ['Texas ', 'TX', 75001, 75501],
    ['Texas', 'TX', 75503, 79999],
    ['Texas', 'TX', 88510, 88589],
    ['Utah', 'UT', 84001, 84784],
    ['Virginia', 'VA', 20040, 20041],
    ['Virginia', 'VA', 20040, 20167],
    ['Virginia', 'VA', 20042, 20042],
    ['Virginia', 'VA', 22001, 24658],
    ['Vermont', 'VT', 5001, 5495],
    ['Vermont', 'VT',  5601, 5907],
    ['Washington', 'WA', 98001, 99403],
    ['Wisconsin', 'WI', 53001, 54990],
    ['West Virginia', 'WV', 24701, 26886],
    ['Wyoming', 'WY', 82001, 83128],
    ['Canada', 'CDN', 1, 1],
    ['Israel', 'ISR', 2, 2],
    ['United Arab Emirates', 'UAE', 3, 3],
    ['United Kingdom', 'UK', 4, 4],
    ['Japan', 'JAP', 5,5]
    #[country, code, number, number]  add extra country
    ]
country_idx = len(zip_code_list) - zip_code_list[-1][-1]
country_code = [[i][0][0] for i in zip_code_list[country_idx:]]
country_str = '* Non-US codes:\n'
for i in zip_code_list[country_idx:]:
    country_str += f'{[i][0][0]} = {[i][0][3]}\n'


def find_state(zip_var):
    global zip_code_list
    state = ''
    state_code = ''

    for i in range(len(zip_code_list)):
        if zip_code_list[i][2] <= zip_var <= zip_code_list[i][3]:
            # state = zip_code_list[i][0]
            state_code = f'{zip_code_list[i][0]}, {zip_code_list[i][1]}'
            break
        else:
            state_code = 'Invalid zip code'
    return state_code




if __name__ == "__main__":
    main()
