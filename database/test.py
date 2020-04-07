#%%
import database as db 


#%%
# engine.execute('alter table table_name add column column_name String')

user_id = 2122
name = 'Johnathan'

db.User.exists()

new_user = db.User(
    user_id=user_id, 
    name=name
    )
new_user.commit()


user_id = message.json.user.id 
name = message. json.user.name

#%%
user_id = 2122
name = 'Johnathan'

#### this is for the start
fcx_user = db.User(
    user_id=user_id, 
    name=name
    )
# check if user exists if true checks for language else commits
if fcx_user.exists():

    welcome_text = {
        f'welcome back {fcx_user.name}'
    }
    # checks if user sets langauge
    if fcx_user.language not in ['en', 'it']:
        print('show_language(message)')
    else:
        print('show_welcome()')

else:
    # outcome is false
    print('show_language(message)')
    fcx_user.commit
    welcome_text = {
        f"welcome to fcx {fcx_user.name}"
    }
    print('show_welcome()')


# %%
