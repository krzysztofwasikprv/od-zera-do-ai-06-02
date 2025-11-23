
# Hobby
col_names_hobby_orig_pl = {
    'hobby_art': 'H Sztuka', 
    'hobby_books': 'H Książki', 
    'hobby_movies': 'H Filmy',
    'hobby_sport': 'H Sport',
    'hobby_video_games': 'H Gry video',
    'hobby_other': 'H Inne',
    }
col_names_hobby_orig_pl_reverse = {v: k for k, v in col_names_hobby_orig_pl.items()}

# Motywacja
col_names_motivation_orig_pl = {
    'motivation_career': 'M Kariera', 
    'motivation_challenges': 'M Wyzwania', 
    'motivation_creativity_and_innovation': 'M Kreatywność i innowacje',
    'motivation_money_and_job': 'M Pieniądze i praca',
    'motivation_personal_growth': 'M Rozwój osobisty',
    'motivation_remote': 'M Praca zdalna',
    }
col_names_motivation_orig_pl_reverse = {v: k for k, v in col_names_motivation_orig_pl.items()}

# Preferowane sposoby nauki
col_names_learn_pref_orig_pl = {
    'learning_pref_books': 'PN Książki', 
    'learning_pref_chatgpt': 'PN Chat GPT', 
    'learning_pref_offline_courses': 'PN Kursy offline',
    'learning_pref_online_courses': 'PN Kursy online',
    'learning_pref_personal_projects': 'PN Projekt własny',
    'learning_pref_teaching': 'PN Nauczanie',
    'learning_pref_teamwork': 'PN Praca zespołowa',
    'learning_pref_workshops': 'PN Warsztaty',
    }
col_names_learn_pref_orig_pl_reverse = {v: k for k, v in col_names_learn_pref_orig_pl.items()}

col_names_other_orig_pl = {
    'age': 'Wiek',
    'age_mid': 'Wiek średni',
    'gender_txt': 'Płeć',
    'gender': "Płeć nr",
    'edu_level': 'Wykształcenie',
    'edu_level_number': 'Wykształcenie nr',
    'industry': 'Branża',
    'years_of_experience': 'Doświadczenie',
    'fav_place': 'Ulubione miejsce',
    'fav_animal_emoji': 'Ulubione zwierzęta', 
    'sweet_or_salty_pl': 'Słodkie \ słone',
    'sweet_or_salty_number': 'Słodkie \ słone nr',
    }

show_cols_table = [
    col_names_other_orig_pl['age'],
    col_names_other_orig_pl['gender_txt'],
    col_names_other_orig_pl['edu_level'],
    col_names_other_orig_pl['industry'],
    col_names_other_orig_pl['years_of_experience'],
    col_names_other_orig_pl['fav_place'],
    col_names_other_orig_pl['fav_animal_emoji'],
    col_names_other_orig_pl['sweet_or_salty_pl'],
]
show_cols_table.extend(col_names_learn_pref_orig_pl.values())
show_cols_table.extend(col_names_motivation_orig_pl.values())
show_cols_table.extend(col_names_hobby_orig_pl.values())

columns_to_plot = [
    'age',
    'gender_txt',
    'edu_level',
    'industry',
    'years_of_experience',
    'fav_place',
    'sweet_or_salty_pl',
]

columns_to_corr = [
    col_names_other_orig_pl['age_mid'],
    col_names_other_orig_pl['gender'],
    col_names_other_orig_pl['edu_level_number'],
    col_names_other_orig_pl['sweet_or_salty_number'],
]
columns_to_corr.extend(col_names_learn_pref_orig_pl.values())
columns_to_corr.extend(col_names_motivation_orig_pl.values())
columns_to_corr.extend(col_names_hobby_orig_pl.values())