<div align="center">
  ![img](https://user-images.githubusercontent.com/87245315/132034660-b4cc8b20-8812-41e3-b505-75d7a6964497.png)
  </p> <br> </p>
</div>
# pdfize-Gui
Pencereli kullanıcı ara yüzü ile resimlerinizden PDF dosyası oluşturun.

# Kullanım
## Dosyaların seçilmesi
### Klasör seç düğmesi ile dosya seçilmesi
- 'Kontroller' bölümündeki ' Klasör seç' butonu ile klasör seçmeniz durumunda, seçtiğiniz dizindeki tüm resimler PDF yapımında kullanılacaktır. Fakat, bu dizinin alt klasörlerindeki resimler kullanılmayacaktır.
- 'Klasör seç' seçeneğinin kullanılması durumunda, klasördeki resimler PDF' e çevrilirken dosyaların sırası 'pkg_resources.parse_version()' gömülü python fonksiyonu kullanılarak otomatik olarak belirlenecektir.
### Dosya seç düğmesi ile dosya seçilmesi
Açılan dosya seçim penceresinden seçtiğiniz resimler kullanılacaktır. PDF oluşturulurken gözetilecek sıra ise sizin dosyaları seçme sıranız ile aynı olacaktır.
### Dosyaları sürükleyip bırakmak
- PDF'e çevirmek istediğiniz dosyaları uygulama penceresine sürükleyip bırakabilirsiniz. Bu sayede uyumlu uzantılara sahip dosyalar otomatik olarak PDF yapma listesine eklenir. Eğer yeni bir dosya grubu sürükleyip bırakılırsa, PDF oluşturma listesi bu dosyalarla değiştirilir.
## Yapılandırma
### Sayfa numarası
- Sayfa numarası olarak numaralar ( 1, 2, 3...) ya da  dosya isimlerini kullanabilirsiniz.
- Sayfa numaralarının metin rengini ve arka plan rengini değiştirebilirsiniz.
- Sayfa numaralarının büyüklüğünü (punto) ve konumunu ayarlayabilirsiniz.
### Filigran
- Bu menüden PDF' inize bir filigran ekleyebilirsiniz.
- Filigran eklenmesi durumunda filigranın; rengini, yazı boyutunu (punto),  ve açısını ayarlayabilirsiniz. Açının birimi derecedir ve yönü yatay eksenden başlayacak şekilde saat yönünün tersinedir.  
### Kırp
- Bu menüden resimleri isteğiniz dahilinde kırpabilirsiniz. Bu bölümdeki rakamların birimi pikseldir.
### Diğer
#### DPI
- varsayılan DPI değeri 100' dür. 
- DPI, dosyanın kalitesi ya da boyutunu etkilemez.
- Sadece PDF okuyucu uygulamalarda sayfaların yakınlaştırma düzeyinin ayarlanmasında kullanılır.
#### Kalite
- Varsayılan değeri 80' dir.
- Daha yüksek değerler kaliteyi artırabilmesine rağmen dosya büyüklüğü de artacaktır.

# Referanslar & Lisans
Bu kısım sadece İngilizce olarak mevcuttur. 
## Pillow
https://github.com/python-pillow/Pillow/blob/master/LICENSE

The Python Imaging Library (PIL) is	 
  
 Copyright © 1997-2011 by Secret Labs AB	 
  
 Copyright © 1995-2011 by Fredrik Lundh	 
    
Pillow is the friendly PIL fork. It is	 
 	 
Copyright © 2010-2021 by Alex Clark and contributors	 
  
Like PIL, Pillow is licensed under the open source HPND License:	 
  
By obtaining, using, and/or copying this software and/or its associated	 
documentation, you agree that you have read, understood, and will comply	 
with the following terms and conditions:	 
  
Permission to use, copy, modify, and distribute this software and its	 
associated documentation for any purpose and without fee is hereby granted,	 
provided that the above copyright notice appears in all copies, and that	 
both that copyright notice and this permission notice appear in supporting	 
documentation, and that the name of Secret Labs AB or the author not be	 
used in advertising or publicity pertaining to distribution of the software	  
without specific, written prior permission.	 
 	 
SECRET LABS AB AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS	   
SOFTWARE, INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.	  
IN NO EVENT SHALL SECRET LABS AB OR THE AUTHOR BE LIABLE FOR ANY SPECIAL,	  
INDIRECT OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM	  
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE	  
OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR	 
PERFORMANCE OF THIS SOFTWARE.

## Psutil
https://github.com/giampaolo/psutil/blob/master/LICENSE

BSD 3-Clause License	 
  
Copyright (c) 2009, Jay Loden, Dave Daeschler, Giampaolo Rodola'	 
  
All rights reserved.	 
  
Redistribution and use in source and binary forms, with or without modification,	 
are permitted provided that the following conditions are met:	 
    
 * Redistributions of source code must retain the above copyright notice, this	 
 list of conditions and the following disclaimer.	 
 * Redistributions in binary form must reproduce the above copyright notice,	 
 this list of conditions and the following disclaimer in the documentation	  
 and/or other materials provided with the distribution.	 
 * Neither the name of the psutil authors nor the names of its contributors	 
 may be used to endorse or promote products derived from this software without	 
 specific prior written permission.	 
  
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND	 
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED	 
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE	  
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR	 
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES	  
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;	 
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON	  
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT	 
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS	  
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
