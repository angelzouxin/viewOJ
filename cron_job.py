
if __name__ == '__main__':
    from static.utils.acManager import AcManager
    from static.utils import ratingUtil
    print('start crawler!')
    AcManager.run()   
    print('end')
    print('start calculate rating!')
    ratingUtil.calculateUsersRating()
    print('end')