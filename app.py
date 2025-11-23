import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

import my_structures as ms
import plot_tools as pt

df = pd.read_csv('35__welcome_survey_cleaned.csv', sep=';')

st.set_page_config(layout="wide")
theme = st.get_option("theme.base") # do dopasowania kolorystyki

radio_options2 = ['All', 'Any']

#region Przygotowanie kolumn Wieku
# Konwersja przedziałów wiekowych w string na dwie osobne kolumny. Dzięki temu można będzie operować na liczbach.
def age_interval_to_numeric(age_str: str):
    if age_str.startswith('<'):
        return (0, int(age_str[1:]))
    if '>=' in age_str:
        return (int(age_str.replace('>=', '')), 100)
    if age_str == 'unknown':
        return (None, None) 
    min_age, max_age = age_str.split('-')
    return (int(min_age), int(max_age))


df['age'].fillna('unknown', inplace=True)
df['age_min'], df['age_max'] = zip(*df['age'].map(age_interval_to_numeric))

# Listy wartości przedziałów wiekowych na slider.
age_values_1  = df['age_min'].dropna().sort_values().unique().tolist()
age_values_2  = df['age_max'].dropna().sort_values().unique().tolist()
age_values = list(set(age_values_1) | set(age_values_2))
age_values.sort()
df['age_mid'] = (df['age_min'] + df['age_max']) / 2
#endregion

#region Przygotowanie kolumn Lat doświadczenia
# Konwersja przedziałów wiekowych w string na dwie osobne kolumny. Dzięki temu można będzie operować na liczbach.
df['years_of_experience'].fillna('unknown', inplace=True)
df['year_exp_min'], df['year_exp_max'] = zip(*df['years_of_experience'].map(age_interval_to_numeric))

# Listy wartości przedziałów wiekowych na slider.
year_exp_values_1  = df['year_exp_min'].dropna().sort_values().unique().tolist()
year_exp_values_2  = df['year_exp_max'].dropna().sort_values().unique().tolist()
year_exp_values = list(set(year_exp_values_1) | set(year_exp_values_2))
year_exp_values.sort()
df['year_exp_mid'] = (df['year_exp_min'] + df['year_exp_max']) / 2
#endregion

#region Przygotowanie kolumn Ulubionych zwierząt.
def split_animals(x):
    if 'Koty' in x and 'Psy' in x:
        return ['Koty', 'Psy']
    else:
        return [x]

animal_tag_emoji = {
    'Koty': '🐱',
    'Psy': '🐶',
    'Inne': '❓',
    'Brak ulubionych': '❌'
}
# Do prezentacji zwierząt w tabeli jako ikony 
def animal_tag_to_emoji(tags):
    return [animal_tag_emoji.get(tag, '🚫') for tag in tags]

# Zwierzęta jako tagi. 
df['fav_animal_tags'] = df['fav_animals'].apply(split_animals)
fav_animal_tags = df['fav_animal_tags'].explode().unique()

for animal in fav_animal_tags:
    df[animal] = df['fav_animal_tags'].apply(lambda x: 1 if animal in x else 0)

# Dodano ikony do prezentacji zwierząt
df['fav_animal_emoji'] = df['fav_animal_tags'].apply(animal_tag_to_emoji)
#endregion

# region Przygotowanie kolumny Ulubionego miejsca
# Zamiana Nan na nazwę przyjazną użytkownikowi 
df['fav_place'] = df['fav_place'].fillna('Brak ulubionego')
fav_place = df['fav_place'].unique()
#endregion

# region Przygotowanie kolumny Płeć
gender_dic = {0: 'Kobieta', 1: 'Mężczyzna'}
gender_val = gender_dic.values()
df['gender_txt'] = df['gender'].map(gender_dic)
#endregion

# region Przygotowanie kolumny Słodkie czy słone
sos_dic = {'sweet': 'Słodkie', 'salty': 'Słone', None: 'Nie wiem'}
sos_val = sos_dic.values()
df['sweet_or_salty_pl'] = df['sweet_or_salty'].map(sos_dic)
df['sweet_or_salty_pl'].fillna(sos_dic[None], inplace=True)

sos_map = { 'sweet': 0, 'salty': 1 }
df['sweet_or_salty_number'] = df['sweet_or_salty'].map(sos_map) #do macierzy korelacji
#endregion

#region Przygotowanie kolumn Preferencje nauki
for col in ms.col_names_learn_pref_orig_pl.keys():
    df[col] = df[col].astype(bool) # konwersja na typ bool
#endregion 

#region Przygotowanie kolumn Motywacja
for col in ms.col_names_motivation_orig_pl.keys():
    df[col] = df[col].astype(bool) # konwersja na typ bool
#endregion 

#region Przygotowanie kolumn hobby
for col in ms.col_names_hobby_orig_pl.keys():
    df[col] = df[col].astype(bool) # konwersja na typ bool
#endregion 

#region Przygotowanie kolumny Branża
df['industry'].fillna('Inna', inplace=True)
industry_val = df['industry'].dropna().unique()
industry_val.sort()
#endregion

#region Przygotowanie kolumny Wykształcenie
mapping = {'Podstawowe': 1, 'Średnie': 2, 'Wyższe': 3}
df['edu_level_number'] = df['edu_level'].map(mapping) #do macierzy korelacji

edu_level = df['edu_level'].dropna().unique()
#endregion

df_filt = df

with st.sidebar:

    st.header('Filtry')
    
    with st.form("my_form", border=False):

        age_sel_min, age_sel_max = st.select_slider(
            "Wiek", 
            options=age_values,
            value=(int(df['age_min'].min()), int(df['age_max'].max())),
        )

        gender_sel = st.multiselect(ms.col_names_other_orig_pl['gender_txt'], gender_val)
        edu_level_sel = st.multiselect(ms.col_names_other_orig_pl['edu_level'], edu_level)
        industry_sel = st.multiselect(ms.col_names_other_orig_pl['industry'], industry_val)

        year_exp_sel_min, year_exp_sel_max = st.select_slider(
            "Doświadczenie", 
            options=year_exp_values,
            value=(int(df['year_exp_min'].min()), int(df['year_exp_max'].max())),
        )

        motivation_key_sel, mot_all_any = pt.pair_multiselect_radio('Motywacja', ms.col_names_motivation_orig_pl.values(), radio_options2, "ms3", "r3")
        learn_key_sel, learn_all_any = pt.pair_multiselect_radio('Preferowany sposób nauki', ms.col_names_learn_pref_orig_pl.values(), radio_options2, "ms2", "r2")

        hobby_sel, hobby_all_any = pt.pair_multiselect_radio('Hobbi', ms.col_names_hobby_orig_pl.values(), radio_options2, "ms4", "r4")
        fav_place_sel = st.multiselect(ms.col_names_other_orig_pl['fav_place'], fav_place)
        fav_animal_tags_sel, animal_all_any = pt.pair_multiselect_radio('Ulubione zwierzęta', fav_animal_tags, radio_options2, "ms1", "r1")
        sos_sel = st.multiselect(ms.col_names_other_orig_pl['sweet_or_salty_pl'], sos_val)

        if st.form_submit_button("Zastosuj"):
            df_filt = df_filt[(df_filt['age_min'] >= age_sel_min) & (df_filt['age_max'] <= age_sel_max)]
            # Jeśli żadne nie wybrane to ignoruj filtr
            if edu_level_sel:
                df_filt = df_filt[df_filt['edu_level'].isin(edu_level_sel)]

            if fav_animal_tags_sel:

                def is_common_tag(tags):
                    if tags:
                        return bool(set(tags) & set(fav_animal_tags_sel))  # True, jeśli jest współny element             
                    else: 
                        return False
                    
                def is_all_tags_equal(tags):
                    if tags:
                        return bool(set(tags) == set(fav_animal_tags_sel))  # True, jeśli jest współny element             
                    else: 
                        return False
                    
                if animal_all_any == radio_options2[0]:
                    df_filt = df_filt[df_filt['fav_animal_tags'].apply(is_all_tags_equal)]
                else:
                    df_filt = df_filt[df_filt['fav_animal_tags'].apply(is_common_tag)]

            if fav_place_sel:
                df_filt = df_filt[df_filt['fav_place'].isin(fav_place_sel)]
            
            if gender_sel:
                df_filt = df_filt[df_filt['gender_txt'].isin(gender_sel)]

            if industry_sel:
                df_filt = df_filt[df_filt['industry'].isin(industry_sel)]

            df_filt = df_filt[(df_filt['year_exp_min'] >= year_exp_sel_min) & (df_filt['year_exp_max'] <= year_exp_sel_max)]

            if sos_sel:
                df_filt = df_filt[df_filt['sweet_or_salty_pl'].isin(sos_sel)]

            if hobby_sel:
                hobby_val_sel = [ms.col_names_hobby_orig_pl_reverse[k] for k in hobby_sel]
                if hobby_all_any == radio_options2[0]:#All
                    df_filt = df_filt[df_filt[hobby_val_sel].eq(1).all(axis=1)]
                else:
                    df_filt = df_filt[df_filt[hobby_val_sel].eq(1).any(axis=1)]

            if motivation_key_sel:
                mot_val_sel = [ms.col_names_motivation_orig_pl_reverse[k] for k in motivation_key_sel]
                if mot_all_any == radio_options2[0]:
                    df_filt = df_filt[df_filt[mot_val_sel].eq(1).all(axis=1)]
                else:
                    df_filt = df_filt[df_filt[mot_val_sel].eq(1).any(axis=1)]

            if learn_key_sel:
                learn_val_sel = [ms.col_names_learn_pref_orig_pl_reverse[k] for k in learn_key_sel]
                if learn_all_any == radio_options2[0]:
                    df_filt = df_filt[df_filt[learn_val_sel].eq(1).all(axis=1)]
                else:
                    df_filt = df_filt[df_filt[learn_val_sel].eq(1).any(axis=1)]


st.header('Przegląd danych ankiety')

col_main1, col_main2 = st.columns([7, 3])

df_filt_pl = df_filt.rename(columns=ms.col_names_other_orig_pl)
df_filt_pl = df_filt_pl.rename(columns=ms.col_names_learn_pref_orig_pl)
df_filt_pl = df_filt_pl.rename(columns=ms.col_names_motivation_orig_pl)
df_filt_pl = df_filt_pl.rename(columns=ms.col_names_hobby_orig_pl)

with col_main1:
    with st.expander('Tabela'):
        st.dataframe(df_filt_pl[ms.show_cols_table], hide_index=True)
    
    with st.expander('Korelacje'):
        corr_matrix = df_filt_pl[ms.columns_to_corr].corr()
        corr_matrix = corr_matrix.abs()
        np.fill_diagonal(corr_matrix.values, 0)

        corr_threshold_min, corr_threshold_max = st.slider(
            "Współczynnik korelacji", 
            min_value=0.0, max_value=1.0, value=(0.0, 1.0),
        )
        cols_to_keep = corr_matrix.columns[((corr_matrix >= corr_threshold_min) & (corr_matrix <= corr_threshold_max)).any()]
        filtered_corr_matrix = df_filt_pl[cols_to_keep].corr()

        pt.plot_heatmap(filtered_corr_matrix)

with col_main2:

    for col in ms.columns_to_plot:
        with st.expander(ms.col_names_other_orig_pl[col]):
            pt.plot_col_hist(df_filt_pl[ms.col_names_other_orig_pl[col]].value_counts(), theme)

    with st.expander('Hobbi'):
        pt.plot_col_hist(df_filt_pl[ms.col_names_hobby_orig_pl.values()].sum().sort_values(ascending=False), theme)

    with st.expander('Motywacja'):
        pt.plot_col_hist(df_filt_pl[ms.col_names_motivation_orig_pl.values()].sum().sort_values(ascending=False), theme)

    with st.expander('Preferowany sposób nauki'):
        pt.plot_col_hist(df_filt_pl[ms.col_names_learn_pref_orig_pl.values()].sum().sort_values(ascending=False), theme)

    with st.expander('Ulubione zwierzęta'):
        pt.plot_col_hist(df_filt_pl[fav_animal_tags].sum().sort_values(ascending=False), theme)
