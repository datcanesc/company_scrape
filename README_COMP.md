Bu dosya içerisinde 4 adet docker-compose.yaml dosyası bulunmaktadır.

Selenium: docker-compose.selenium.yaml
Company Finder : docker-compose.company_finder.yaml
Company Scrape : docker-compose.company_scrape.yaml
Neo4j Upload : docker-compose.neo4j_upload.yaml


Selenium yaml dosyası Company Finder ve Company Scrape yaml dosyalarının çalışması için öncelikle başlatılamsı gerekmektedir. 

1-) Seleniumun başlatılması

!!! Bu işleme başlamadan önce config dosyasından gerekli url'ler değiştirlmelidir.
- Selenium'u başlatmak için :
docker-compose -f docker-compose.selenium.yaml up



2-) Company Finder'ın başlatılması
Selenium başlatıldıktan sonra öncelike Company Finder yaml dosyası başlatılır. Company Finder the Org sitesi içerisindeki her bir ülkedeki şirketlerin linklerini bulur ve bunu bir txt dosyasında depolar. Depoladığı linkler company_urls_data klasörü içerisinde txt dosyasında bulunmaktadır. Bu işlemin bitmesi uzun sürebilir ancak the Org günlük olarak güncellenmediği için uzun aralıklarla çalıştırılması daha uygun olacaktır. Programın her hangi bir hata sebebiyle sonlanması durumunda yeniden compose up edilmesi bir sıkıntı çıkartmayacaktır. (Aynı linkleri birden fazla yazma vb.)

Dikkat:
Company Finderın bittiğinden emin olmak için company_url_data klasörünün içerisindeki last_processed.txt dosyasındaki ülke koduna bakılabilir. Eğer "ZW" üle kodu varsa işlevini tamamlamıştır.

- Company Finder'ı başlatmak için:
docker-compose -f docker-compose.company_finder.yaml up


3-) Company-Scrape'nin başlatılması
Company Finder'ın işlemleri bittikten sonra the Org içerisindeki güncel olan bütün şirketlerin linkleri bir txt dosyasında olacaktır. Bu adımdan sonra Company Scrape yaml dosyasının çalıştırlmalıdır. Bu işlem uzun sürebilir, çünkü her bir şirket içerisindeki her bir kişinin profilini tek tek scrapeleyecektir. Bu scrapelenen şirketlerin bilgileri company_data klasörü içerisinde tutulmaktadır. company.json dosyası içerisinde scrapelenen şirketlerin bilgileri bulunmaktadır ve scraped_urls.txt dosyasında ise işlemlerin tamamlandığı sitelerin linkleri yazmaktadır. 

- Company Scrape çalıştırmak için
docker-compose -f docker-compose.company_scrape.yaml up


4-) Verilerin Neo4j'ye aktarılması

!!! Bu işleme başlamadan önce config dosyasından gerekli url'ler değiştirlmelidir.

Company-Scrape işlemi bittikten sonra Neo4j Upload yaml dosyası çalıştırlımalıdır. Bu kod company.json içerisindeki şirket bilgilerini Neo4jye aktarır. Aktarılma sürecinde bir sıkıntı çıkması durumunda dosya yeniden compose up yapılarak veri aktarılmaya devam edilebilir. Neo4j aynı şirket verilerinin bir daha yazılmasını engellemektedir.


- Neo4j Upload çalıştırılması
docker-compose -f docker-compose.neo4j_upload.yaml up





Yukarıda bahsedilen işlemlerin sürekli olarak tekrarlanması yanlış olacaktır çünkü the Org sitesi günlük olarak güncellenmemektedir. Bu yüzden işlemlerin bir defa yapılması site içerisindeki bir çok şirketin bilgilerini almaya yetecektir. Eksik olduğunu düşündüğünüz veya siteye yeni eklenen şirketler olması durumunda programın yeniden çalıştırılması doğru olacaktır.



