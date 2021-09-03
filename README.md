![img hq](https://user-images.githubusercontent.com/87245315/132034535-177a3084-b321-439e-abc4-b72001e6cce0.png)
# pdfize-Gui
Create a pdf file from your images with the help of the graphical user interface.

# Usage
## Selecting files
### Using select folder button
- You may use the select folder button in the 'Controls' section. By doing this, all the image files in that directory will be used to create the PDF. However, if this folder contains subfolders, the images in the subfolders will not be used. Moreover, you may alter the default input folder, the folder automatically chosen at the startup of the application, from Menu>App settings>Default input folder>Change.
- If you use the 'Select folder' option, the images in the folder will be automatically sorted using the 'pkg_resources.parse_version()' built-in python function.
### Using select files button
The images you selected in the file dialog will be used to create the PDF. The order of the pictures in PDF will be the same as your order of selection.
## Configuring
### Page number
- You may use either integer ( 1, 2, 3...) or filenames as the page numbers.
- You may edit the background and foreground colors of page numbers.
- You can edit the point size and position of the page numbers.
### Watermark
- You may insert a watermark from this menu.
- If the watermark is enabled, you can change its color, font size, and angle (direction is counterclockwise starting from the horizontal axis, unit is degrees)
### Cropping
- You can crop images in this menu. The unit of parameters in this menu is pixels.
### Other
#### DPI
- The default value of the DPI is 100. 
- It never affects the file size and quality.
- It only determines the zoom level of the pages in the PDF reader application.
#### Fidelity
- Its default value is 80.
- Higher values may increase the quality; however, the file size also may increase.


# References & License
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
