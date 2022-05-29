import logging
from environs import Env

env = Env()
env.read_env()
TOKEN = env.str('TOKEN')

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


from telegram.ext import Updater, CallbackContext, CommandHandler, Dispatcher, ConversationHandler, MessageHandler, \
    Filters
from telegram import Update, ReplyKeyboardMarkup


USERTYPE, MENTORACTIONS, CREATEGROUP = range(3)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Choose as who you want to login?',
        reply_markup=ReplyKeyboardMarkup([
            ['Mentor'], ['Student']
        ], resize_keyboard=True)
    )
    return USERTYPE


def mentor(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='You are mentor',
        reply_markup=ReplyKeyboardMarkup([
            ['Create group'], ['My groups']
        ], resize_keyboard=True)
    )
    return MENTORACTIONS


def add_group(update: Update, context: CallbackContext):
    group = update.message.text
    update.message.reply_text(
        text=f'You created group {group}'
    )
    return MENTORACTIONS


def student(update: Update, context: CallbackContext):
    # MessageHandler(Filters.regex('^(Back)$'), back)
    update.message.reply_text(
        text='You are student',
        reply_markup=ReplyKeyboardMarkup([
            ['Join Group'], ['My groups']
        ], resize_keyboard=True)
    )
    return 3


def create_group(update: Update, context: CallbackContext):
    update.message.reply_text('Write name of your group?')
    return CREATEGROUP


def join_group(update: Update, context: CallbackContext):
    pass


def my_groups(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='\n'.join([f'{idx}. {group}' for idx, group in enumerate(['first group', 'second group'], start=1)])
    )


updater = Updater(TOKEN)
dp: Dispatcher = updater.dispatcher

dp.add_handler(ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        USERTYPE: [
            MessageHandler(Filters.regex('^(Mentor)$'), mentor),
            MessageHandler(Filters.regex('^(Student)$'), student),
        ],
        MENTORACTIONS: [
            MessageHandler(Filters.regex('^(Create group)$'), create_group),
            MessageHandler(Filters.regex('^(My groups)$'), my_groups),
        ],
        CREATEGROUP: [MessageHandler(Filters.text, add_group)],
    },
    fallbacks=[MessageHandler(Filters.regex('^(Main)$'), start)]
))

updater.start_polling()
updater.idle()
