from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Item, User, Basketz

engine = create_engine("sqlite:///productcatalog.db")
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won"t be persisted into the database until you call
# session.commit(). If you"re not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


TV1=Item(section="Electronics", itemtype="TV", description="Element 50 4K UHD 60Hz Smart TV", size="50", brand="Element", image="target.scene7.com/is/image/Target/52495781_Alt01", price="$249.99", rating="2.9")
TV2=Item(section="Electronics", itemtype="TV", description="Element 50 4K UHD Smart TV - Amazon Fire TV Edition - Black (EL4KAMZ501)", size="50", brand="Element", image="target.scene7.com/is/image/Target/52475682_Alt01", price="$299.99", rating="1.5")
TV3=Item(section="Electronics", itemtype="TV", description="Element 55 4K UHD 60Hz Smart TV", size="55", brand="Element", image="target.scene7.com/is/image/Target/52495829_Alt01", price="$649.99", rating="1.4")
TV4=Item(section="Electronics", itemtype="TV", description="Element 55 4K UHD Smart TV - Amazon Fire TV Edition - Black (EL4KAMZ5517T)", size="55", brand="Element", image="target.scene7.com/is/image/Target/52475720_Alt01", price="$379.99", rating="0.3")
TV5=Item(section="Electronics", itemtype="TV", description="LG 55 Class 2160p 4K Ultra HD HDR Smart OLED TV - OLED55B7A", size="55", brand="LG", image="target.scene7.com/is/image/Target/52328755_Alt01", price="$899.99", rating="2.9")
TV6=Item(section="Electronics", itemtype="TV", description="LG 55 Class 2160p 4K Ultra HD Smart LED TV - 55UJ6300", size="55", brand="LG", image="target.scene7.com/is/image/Target/51972816_Alt01", price="$299.99", rating="0.6")
TV7=Item(section="Electronics", itemtype="TV", description="LG 49 4K Ultra HD Smart LED TV", size="49", brand="LG", image="target.scene7.com/is/image/Target/52702277_Alt01", price="$169.99", rating="1.0")
TV8=Item(section="Electronics", itemtype="TV", description="Samsung 49 UHD - 49MU6290", size="49", brand="Samsung", image="target.scene7.com/is/image/Target/52760283_Alt01", price="$129.99", rating="1.5")
TV9=Item(section="Electronics", itemtype="TV", description="Samsung 50 Smart UHD 4K 120 Motion Rate TV - UN50MU6300FXZA", size="50", brand="Samsung", image="target.scene7.com/is/image/Target/50714354_Alt01", price="$379.99", rating="4.5")
TV10=Item(section="Electronics", itemtype="TV", description="Samsung 55 4k UHD TV - Black (UN55MU7000)", size="55", brand="Samsung", image="target.scene7.com/is/image/Target/52352730_Alt01", price="$299.99", rating="0.9")
TV11=Item(section="Electronics", itemtype="TV", description="Samsung 55 Curved Smart UHD 4K 120 Motion Rate TV - 55MU6490", size="55", brand="Samsung", image="target.scene7.com/is/image/Target/50672694_Alt01", price="$349.99", rating="1.4")
TV12=Item(section="Electronics", itemtype="TV", description="Samsung 58 4K UHD Smart TV - 58MU6100", size="58", brand="Samsung", image="target.scene7.com/is/image/Target/52720842_Alt01", price="$125.99", rating="3.1")
TV13=Item(section="Electronics", itemtype="TV", description="Samsung 55 Class 2160p 4K Smart Ultra HD TV - 55MU6290", size="55", brand="Samsung", image="target.scene7.com/is/image/Target/17220013_Alt01", price="$219.99", rating="3.6")
TV14=Item(section="Electronics", itemtype="TV", description="TCL 43 4K HDR 120Hz CMI Roku Smart LED TV - Black (43S405)", size="43", brand="TCL", image="target.scene7.com/is/image/Target/52177069_Alt01", price="$349.99", rating="2.6")
TV15=Item(section="Electronics", itemtype="TV", description="TCL 49 4K UHD HDR Roku Smart TVPolaroid 43 4K UHD LED TV with Chromecast Built-in", size="49", brand="TCL", image="target.scene7.com/is/image/Target/52177113_Alt01", price="$109.99", rating="2.1")
TV16=Item(section="Electronics", itemtype="TV", description="TCL 55 4K 120Hz CMI Roku Smart LED TV - Black (55S405)", size="55", brand="TCL", image="target.scene7.com/is/image/Target/50480469_Alt01", price="$229.99", rating="3.2")
TV17=Item(section="Electronics", itemtype="TV", description="VIZIO SmartCast E-series 50 Class 4K Ultra HD Home Theater Display with Chromecast Built-in- Black (E50-E3)", size="50", brand="VIZIO", image="target.scene7.com/is/image/Target/51754022_Alt02", price="$349.99", rating="3.1")
TV18=Item(section="Electronics", itemtype="TV", description="VIZIO D-Series 43 Class 42.51 Diag. 2160p 120Hz Ultra HD Full-Array LED Smart TV - D43-E2", size="43", brand="VIZIO", image="target.scene7.com/is/image/Target/52229025_Alt01", price="$512.99", rating="2.8")
TV19=Item(section="Electronics", itemtype="TV", description="VIZIO D-series 50 Class 49.5 Diag. Ultra HD 120Hz Full-Array LED Smart TV - D50-E1", size="50", brand="VIZIO", image="target.scene7.com/is/image/Target/50651255_Alt01", price="$899.99", rating="2.1")
TV20=Item(section="Electronics", itemtype="TV", description="VIZIO D-Series 55 54.6 Diag. 2160p 120Hz Ultra HD Full-Array LED Smart TV - D55-E0", size="55", brand="VIZIO", image="target.scene7.com/is/image/Target/50651370_Alt01", price="$449.99", rating="1.8")
TV21=Item(section="Electronics", itemtype="TV", description="VIZIO SmartCast E-Series 55 Class 54.60 Diag. 2160p 120Hz Ultra HD HDR XLED Display - E55-E1", size="55", brand="VIZIO", image="target.scene7.com/is/image/Target/51753780_Alt02", price="$299.99", rating="1.7")
TV22=Item(section="Electronics", itemtype="TV", description="VIZIO SmartCast M-Series 55 Class 4K Ultra HD HDR XLED Plus Display - M55-E0", size="55", brand="VIZIO", image="target.scene7.com/is/image/Target/52229255_Alt01", price="$449.99", rating="2.7")
TV23=Item(section="Electronics", itemtype="TV", description="Westinghouse 55 4K UHD Smart TV", size="55", brand="Westinghouse", image="target.scene7.com/is/image/Target/52759243_Alt01", price="$249.99", rating="2.8")
TV24=Item(section="Electronics", itemtype="TV", description="Westinghouse 55 4K UHD Smart TV", size="55", brand="Westinghouse", image="target.scene7.com/is/image/Target/52759243_Alt01", price="$249.99", rating="0.8")




# Menu for UrbanBurger
tvs = [TV1,TV2,TV3,TV4,TV5,TV6,TV7,TV8,TV9,TV10,TV11,TV12,TV13,TV14,TV15,TV16,TV17,TV18,TV19,TV20,TV21,TV22,TV23,TV24]

for tv in tvs:
    session.add(tv)
    session.commit()


print "added menu items!"
