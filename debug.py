import users, courses, materials, tasks

def initSetup():
    """ Users, materials and tasks for testing 
    """
    if users.get_user_name(1) != "Test Teacher":
        users.register("Test Teacher", "test123", "teacher")
        courses.create_new("Kanji for beginners part 1", "Learn Japanese Kanji characters (JLPT N5 level)", 1)
        materials.add_material(1, "Kanji no. 1: 日", "日, meaning: the sun, a day. \
                               \n くんよみ (Kunyomi) reading: ひ/-び (hi/-bi), -か (-ka). \
                               \n  オンヨミ (Onyomi) reading: ニチ/ニ (nichi/ni). \
                               \n Examples: 日 , reading: ひ (hi), meaning: the sun, a day. \
                               \n 日本, reading: にほん/にっぽん (nihon/nippon), meaning: Japan")
        materials.add_material(1, "Kanji no. 2: 月", "月, meaning: the moon, a month. \
                               \n くんよみ (Kunyomi) reading: つき (tsuki). \
                               \n オンヨミ (Onyomi) reading: ゲツ/-ガツ (getsu/-gatsu). \
                               \n Examples: 月 , reading: つき (tsuki), meaning: the moon, a month. \
                               \n 一月/1月, reading: いちがつ (ichigatsu), meaning: January")
        materials.add_material(1, "Kanji no. 3: 木", "木, meaning: a tree. \
                               \n くんよみ (Kunyomi) reading: き (ki). \
                               \n オンヨミ (Onyomi) reading: モク, ボク  (moku/boku). \
                               \n Examples: 木 , reading: き (ki), meaning: a tree. \
                               \n 木曜日, reading: もくようび (mokuyoobi), meaning: Thursday")
        materials.add_material(1, "Kanji no. 4: 山", "山, meaning: mountain. \
                               \n くんよみ (Kunyomi) reading: やま (yama). \
                               \n オンヨミ (Onyomi) reading: サン (san). \
                               \n Examples: 山 , reading: やま (yama), meaning: mountain. \
                               \n 富士山, reading: ふじさん (fujisan), meaning: Mt. Fuji")
        tasks.add_task("Which of these Kanji means the sun?", 1 , "multiple choice")
        tasks.add_task_choices(1, ["月", "木", "山", "日"], ["3"])
        tasks.add_task("Which of these Kanji means a mountain?", 1 , "multiple choice")
        tasks.add_task_choices(2, ["月", "木", "山", "日"], ["2"])
        tasks.add_task("Write the Kanji for moon below in romaji (latin script, e.g. 'nihon' )", 1 , "fill in")
        tasks.add_task_choice(3, "tsuki")
        tasks.add_task("Write the Kanji for tree below in romaji (latin script, e.g. 'nihon' )", 1 , "fill in")
        tasks.add_task_choice(4, "ki")

    if users.get_user_name(2) != "Test Student":
        users.register("Test Student", "test123", "student")
