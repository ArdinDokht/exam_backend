import enum


class ExamType(str, enum.Enum):
    TEST = 'تستی'
    DESCRIPTIVE = 'تشریحی'


class QuestionPaperType(str, enum.Enum):
    FULL = 'کامل'
    LESSON_SEPARATE = 'درس'
    LESSON_TYPE_SEPARATE = 'نوع درس'


class ExamLessonType(str, enum.Enum):
    GENERAL = 'عمومی'
    SPECIAL = 'اختصاصی'


class ExamScoreType(str, enum.Enum):
    LESSON = 'درس'
    GENERAL = 'عمومی'
    SPECIAL = 'اختصاصی'
    TOTAL = 'کلی'


class ExamStatusType(str, enum.Enum):
    CLASS_ROOM = 'کلاس'
    SCHOOL = 'مدرسه'
    TOTAL = 'کل'
