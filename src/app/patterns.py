game_finish = r'طول مدت بازی|مدت زمان بازی|مدت بازی|مدت بُکُن بُکُن'
game_list = r'بازیکن های زنده|فراموشکارای زنده|هنرمندای فعال|دانشجوهای مشغول به تحصیل|مسافرای زنده ی توی قطار|بازیکنان زنده|بازیکن های آنلاین|کونده های زنده |بازیکنان درحال بازی|برره ای های زنده|مسافر های زنده:|کشتی گیران سالم|هیولاهای زنده|بازمانده ها'
death = r'مرده|اخراج شده|کنار رفته|آفلاین|تبعید شده|بگا رفته|خارج شده|سقَط شده|فرار کرده|اخراج شده|نفله وشده'
game_started = r'ایول بازی شروع شد 😃|توجه توجه دانشگاه شروع شد|حلقه پیدا شد|قطار داره راه میافته|ژوون بازی شروع شد|WINTER IS HERE|استارت شد ، سیستم در حال ارسال نقش|ژوووووون💦 بازی شروع شد|بالاخره بازی شروع شد|خب بُکُن بُکُن شروع شد|ایول مسابقات شروع شد|خب خب خب . بازی شروع شد|حااا بازی شروع وشد |ایول بازی شروع شد|قطار راه افتاد |بالاخره شروع شد|در های ورودی کمپانی بسته شد|ایول درهای هتل بسته شد|خب رسیدیم میستیک فالز|😍جون جون وایستین بازی شروع شد'
game_canceled = r'کلاس ها تعطیله عزیزان|چقدر کمین!|چقدر شایرخلوته|تعداد مسافران کافی نیست |زرت تعدادتون کمه دیوثا |تعدادتون خیلی کمه😖|با این تعداد آدم میخواین فرمانروایی راه بندازین|چقدر کمین!|کچلم کردین ، اخه با این تعداد |زرشگ فقط همین قدر اصن نوریم برره|متاسفم حداقل باید 5 تا کابوی شرکت کنه|عجیبه! بازیکنان فوتبال میلیون ها دلار کسب می کنند اما اینجا بازیکن کافی ندارد. مسابقات لغو شد'
player_afk = r'دو شب متوالی رای نداده به درد لای جرز میخوره| خوب احتمالا وقتی داشته از بین دو واگن قطار رد میشده افتاده پایین|دو شب متوالی فقط جق میزد از بازی حذف می ش| دو شب متوالی فقط جق میزد به صورت تخماتیک از بازی حذف می شه|دو شبه که هیچ فعالیتی نداشته و تکست یا بیتی رو آماده نکرده باید با موسیقی خداحافظی کنه|کسکشِ جقی دو شب متوالی فقط جق میزد دستاش خسته شد و نتونست بازی کنه برا همین سیکشو زدیم|دو شب متوالی رای نداده به نظر میاد مرده،بیاید دفنش کنیم'
jointime_started = r'ساخته شده فراموش نکنید که روی کادر زیر کلیک کنید تا بتونید وارد بازی شید|ساخته شده روی دکمه وارد شوید کلیک کنید تا بهتون مجوز ورود به روستا رو بدم|هم گارچی بید زودتر سوار وشید|اماده حرکت به سمت برره بید برای سوار شدن دکمه وارد شوید را وزنید|گاریچی شده این گاری خیلی تند وره فقط اگه سوار وشدین مواظب وباشید|گاریچی خوبیه اگه میخوایید سوار وشید وارد شوید رو زودتر وزنید جیگرا|ساخته جوین شین کون گنده ها|ساخته جوین شین آب کونا|سلام امیدوارم که توش باشه|ساخته جوین شین کون پشما|آغاز جنگ با تیتان هارو اعلام کرده|ساخته شده تخمیا یادتون نره که روی کیرخر زیر کلیک کنید تا بتونید کیرمو بخورید و بازی کنید|ساخته شده روی کیر من کلیک کنید تا بهتون مجوز ورود به روستای جقی رو بدم|ساخته شده تخمیا فراموش نکنید که روی کیرخر زیر کلیک کنید تا بتونید کیرمو بخورید و بازی کنید|ساخته شده برای اینکه بلیط بخری روی کادر زیر بزن|ساخته شده برای تهیه بلیط روی دکمه وارد شوید کلیک کنید تا بهتون بلیط ورود به قطار رو بدم|ساخته شده فراموش نکنید که برای تهیه بلیط روی کادر زیر بزنید|ساخته برای تهیه بلیط روی دکمه زیر کلیک کنید تا بهتون مجوز ورود به قطار رو بدم|ساخته شده فراموش نکنید که روی کادر زیر کلیک کنید تا بتونید وارد بازی شید|THE KING IN THE NORTH|ساخته شده روی دکمه وارد شوید کلیک کنید تا بهتون مجوز رپ کردن رو بدم|هتل ترانسیلوانیا رو ساخته!سریعتر بیاین|واسه ورود به غرب وحشی رو دکمه وارد شوید شلیک کن|بپرید توی بازی کسکشا|اووووف یک بازی جدید تو مود مافیا ساخته شده|یه بازی جدید در مود مافیا|و گناهان شهر ریوردیل بشید|بازی شروع بشه|تا بتونیم بازیو شروع کنیم|یه بازی کیری ساخته روی کادر زیر کلیک کنید تا ابکیرمو بخورین و توی بازی جوین شین|روی دکمه وارد شوید کلیک کنید تا بهتون مجوز ورود به بیکینی باتم کیری رو بدم|روی دکمه پایین کلیک کنید تا سیک کنید تو بازی|کصخل یه بازی جدید ساخت هرکی جوین نشه کصکشه|این دکمه کیری پایینو بزنین تا برام ساک بزنین و جوین شین|کصخل یه بازی جدید با حالت آشوب ساخت هرکی جوین نشه کصکشه|رو بزنید تا سوار سفینه بشید|رو بزنین تا وارد هلی کریر بشین از ترینیتی کمیکس|رو بزنین تا وارد هلی کریر بشین|رو بزن تا وارد هلی کریر بشی از ترینیتی کمیکس|رو بزن تا وارد هلی کریر بشی|ساخته شده فراموش نکنید که کنکور بدید تا بتونید وارد دانشگاه شید|بتونید وارد میستیک فالز بشید|ورود به میستیک فالز رو|برای ملحق شدن کلیک کنید|به ما ملحق شو بریم ببینیم توش چه خبره| کلیک کنید تا بتونید وارد شایربشید|بهتون مجوز ورود به شایررو بدم|قطاری رو به ایستگاه فراخونده|فصل فوتبال آغاز شده|برای فوتبال بازی کردن وارد شوید|فصل نامنظم فوتبال آغاز شده|بهتون مجوز ورود به بیکینی باتم رو بدم'


roles_by_emoji = {'👱': {'role_title': 'روستایی', 'role_id': 1}, '🐺': {'role_title': 'گرگینه', 'role_id': 2},
                  '🍻': {'role_title': 'مست', 'role_id': 3}, '👳': {'role_title': 'پیشگو', 'role_id': 4},
                  '😾': {'role_title': 'نفرین شده', 'role_id': 5}, '💋': {'role_title': 'فاحشه', 'role_id': 6},
                  '👁': {'role_title': 'ناظر', 'role_id': 7}, '🔫': {'role_title': 'تفنگدار', 'role_id': 8},
                  '🖕': {'role_title': 'خائن', 'role_id': 9}, '👼': {'role_title': 'فرشته نگهبان', 'role_id': 10},
                  '🕵️': {'role_title': 'کاراگاه', 'role_id': 11}, '🙇': {'role_title': 'پیشگوی رزرو', 'role_id': 12},
                  '👤': {'role_title': 'فرقه گرا', 'role_id': 13}, '💂': {'role_title': 'شکارچی', 'role_id': 14},
                  '👶': {'role_title': 'بچه وحشی', 'role_id': 15}, '🃏': {'role_title': 'احمق', 'role_id': 16},
                  '👷': {'role_title': 'فراماسون', 'role_id': 17}, '🎭': {'role_title': 'همزاد', 'role_id': 18},
                  '💘': {'role_title': 'الهه عشق', 'role_id': 19}, '🎯': {'role_title': 'کلانتر', 'role_id': 20},
                  '🔪': {'role_title': 'قاتل زنجیره ای', 'role_id': 21}, '👺': {'role_title': 'منافق', 'role_id': 22},
                  '🎖': {'role_title': 'کدخدا', 'role_id': 23}, '👑': {'role_title': 'شاهزاده', 'role_id': 24},
                  '🔮': {'role_title': 'جادوگر', 'role_id': 25}, '🤕': {'role_title': 'پسر گیج', 'role_id': 26},
                  '⚒': {'role_title': 'آهنگر', 'role_id': 27}, '⚡️': {'role_title': 'گرگ آلفا', 'role_id': 28},
                  '🐶': {'role_title': 'توله گرگ', 'role_id': 29}, '💤': {'role_title': 'خواب گذار', 'role_id': 30},
                  '🌀': {'role_title': 'پیشگوی نگاتیوی', 'role_id': 31},
                  '👱🌚': {'role_title': 'گرگ نما', 'role_id': 32}, '🐺🌝': {'role_title': 'گرگ ایکس', 'role_id': 33},
                  '☮️': {'role_title': 'صلح گرا', 'role_id': 34}, '📚': {'role_title': 'ریش سفید', 'role_id': 35},
                  '😈': {'role_title': 'دزد', 'role_id': 36}, '🤯': {'role_title': 'دردسرساز', 'role_id': 37},
                  '👨‍🔬': {'role_title': 'شیمیدان', 'role_id': 38},
                  '🐺☃️': {'role_title': 'گرگ برفی', 'role_id': 39}, '☠️': {'role_title': 'گورکن', 'role_id': 40},
                  '🔥': {'role_title': 'آتش زن', 'role_id': 41}, '🦅': {'role_title': 'رمال', 'role_id': 42}}
roles_pattern = r'👱|🐺|🍻|👳|😾|💋|👁|🔫|🖕|👼|🕵️|🙇|👤|💂|👶|🃏|👷|🎭|💘|🎯|🔪|👺|🎖|👑|🔮|🤕|⚒|⚡️|🐶|💤|🌀|👱🌚|🐺🌝|☮️|📚|😈|🤯|👨‍🔬|🐺☃️|☠️|🔥|🦅'