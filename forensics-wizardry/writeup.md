# Wizardry

### Resources

[Explaination of Incremental Saves](https://pspdfkit.com/blog/2019/incremental-and-full-save-in-pdfs/)
[Tool for extracting versions](https://github.com/jesparza/peepdf)

### Analysis

Examining the file, you can notice that there are multiple %%EOF tags. This indicates that somes sort incremental save/generation was used.

Using a tool like peepdf, we can go back to a previous version with the flag

### Other solutions

Apparently, you could just extract the images from the pdf in some cases. I probably should've checked that was possible a bit better than I did. 

### Hints

if you were to add something small (comparatively) like a signature to a document, how could that look?

try looking for pdf specific forensic ideas
specifically if you were to make a small change to your document (like a signature)

### Postmortem

This challenge ended up being one of the easiest due to me not properly de-cheesing the challenge. I think the cheese wouldn't have been an issue if i put more into spitting up the flag image. 

The challenge hint probably could have been a lot better in hindsight - lot of people thought it was about digital signatures. 

It was very annoying to find a pdf library that supported incremental saves. 
