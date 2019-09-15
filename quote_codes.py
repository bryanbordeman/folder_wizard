'''==========================================
Title:  quote_codes.py
Author:  Bryan Bordeman
Start Date:  062219
Updated:  071019
Version:  support script

;=========================================='''


def main():
    '''ONLY FOR TESTING'''
    global category
    # Make list of type based on selected category
    sel_category = 'Security Shielding'  # selected category

    type_list = [i[0] for i in category[sel_category]]
    # for i in category[sel_category]:
    #     type_list.append(i[0])
    print(type_list)

    # set type code based on selected type
    sel_type = 'SCIF'  # selected type
    type_code = category[sel_category][type_list.index(sel_type)][1]
    print(type_code)


category = {'MRI':
            [['GE', 'MRI-GEH'],
             ['Siemens', 'MRI-SEM'],
             ['Philips', 'MRI-PHL'],
             ['Hitachi', 'MRI-HIT'],
             ['Canon', 'MRI-CAN'],
             ['Hallmarq', 'MRI-HLM'],
             ['Components', 'MRI-CMP'],
             ['Cryo Vent', 'MRI-CRY'],
             ['FerrAlert', 'MRI-KOP'],
             ['Other', 'MRI-OTH']],
            'Low Energy Radiation Shielding':
            [['CT Suite', 'LER-CTS'],
             ['X-Ray Suite', 'LER-XRA'],
             ['IR Suite', 'LER-IRS'],
             ['OR Suite', 'LER-ORS'],
             ['PET Suite', 'LER-PET'],
             ['Modular Partition', 'LER-MOD'],
             ['All-Shield', 'LER-ALL'],
             ['Artemis', 'LER-ART'],
             ['Unistrut', 'LER-UNI'],
             ['Components', 'LER-CMP'],
             ['Other', 'LER-OTH']],
            'High Energy Radiation Shielding':
            [['Linac', 'HER-LIN'],
             ['Cyberknife', 'HER-CYB'],
             ['HDR', 'HER-HDR'],
             ['Cyclotron', 'HER-CYC'],
             ['Proton', 'HER-PRO'],
             ['Industrial X-Ray', 'HER-IND'],
             ['Supplemental', 'HER-SUP'],
             ['Swing Door', 'HER-SWG'],
             ['Sliding Door', 'HER-SLD'],
             ['Baffle', 'HER-BAF'],
             ['Artemis', 'HER-ART'],
             ['Other', 'HER-OTH']],
            'Industrial Shielding':
            [['AC/ELF', 'IND-ELF'],
             ['High-Spec RF Shielding', 'IND-656'],
             ['Partial Discharge', 'IND-PDI'],
             ['Anechoic Chamber', 'IND-ANC'],
             ['PIM', 'IND-PIM'],
             ['HEMP', 'IND-HMP'],
             ['Synchrotron', 'IND-SYC'],
             ['X-Ray Cabinet', 'IND-XRC'],
             ['RF Cabinet', 'IND-RFC'],
             ['Other', 'IND-OTH']],
            'Security Shielding':
            [['SCIF', 'SEC-SCI'],
             ['High-Spec RF Shielding', 'SEC-656'],
             ['Other', 'SEC=OTH']],
            'Engineering':
            [['RF Shield Design', 'SVE-RFD'],
             ['Magnetic Shield Design', 'SVE-MAG'],
             ['Physics Design', 'SVE-RAD'],
             ['Other', 'SVE-OTH']],
            'Testing':
            [['RF Testing', 'SVT-RFT'],
             ['High-Spec Testing', 'SVT-HST'],
             ['Vibration Testing', 'SVT-VIB'],
             ['Other', 'SVT-OTH']],
            'Door Service':
            [['RF Door Service', 'SVC-RFS'],
             ['Radiation Door Service', 'SVC-PBS'],
             ['Other', 'SVC-OTH']],
            'GPS Specialty Doors':
            [['Blast Door', 'GPS-BLT'],
             ['Studio Door', 'GPS-STD'],
             ['Ballistic Doors','GPS-BLC'],
             ['Elephant Doors', 'GPS-ELP'],
             ['Hangar Doors', 'GPS-HAG'],
             ['Large Radiation Door', 'GPS-RAD'],
             ['Large RF Door', 'GPS-RFD'],
             ['Security Door', 'GPS-SEC'],
             ['Other', 'GPS-OTH']],
            'Other':
            [['Other', 'OTH-OTH']]
            }


# category_list = [i for i in category.keys()]


if __name__ == "__main__":

    # for testing only not used in app
    main()
