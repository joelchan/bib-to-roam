{
    "translatorID":"dda092d2-a257-46af-b9a3-2f04a55cb04f",
    "translatorType":2,
    "label":"Roam Metadata Export",
    "creator":"Joel Chan",
    "target":"md",
    "minVersion":"2.0",
    "maxVersion":"",
    "priority":200,
    "inRepository":false,
    "lastUpdated":"2020-08-29 - 10:15"
    }
     
    function doExport() {
      var item;
      while (item = Zotero.nextItem()) {
        var creatorsS = item.creators[0].lastName;
        if (item.creators.length>2) {
          creatorsS += " et al.";
        } else if (item.creators.length==2) {
          creatorsS += " & " + item.creators[1].lastName;    
        }
     
        var citationKey = (item.citationKey) ? item.citationKey : "(bib citkey missing)";
        
        // ref
        Zotero.write('[[@' + item.citationKey + ']]\n');
    
        // top level block
        Zotero.write('\t - #[[references]]\n');
    
        // title
        var titleS = (item.title) ? item.title : "(no title)";
        Zotero.write('\t\t- Title: ' + titleS + '\n');
    
        // meta block
        Zotero.write('\t\t- Meta:\n');
    
        // author
        Zotero.write('\t\t\t- Authored by:: ');
        for (author in item.creators){
          Zotero.write('[[' + item.creators[author].firstName + ' ' + item.creators[author].lastName + ']] ');
        }
        Zotero.write('\n');
     
        // year
        var date = Zotero.Utilities.strToDate(item.date);
        var dateS = (date.year) ? date.year : item.date;   
        Zotero.write('\t\t\tYear: ')
        Zotero.write('[[' + dateS + ']]\n')
        
        // publication
        Zotero.write('\t\t\tPublication: ')
        Zotero.write(item.publicationTitle + '\n')
     
        // zotero link
        var library_id = item.libraryID ? item.libraryID : 0;  
        var itemLink = 'zotero://select/items/' + library_id + '_' + item.key;
     
        Zotero.write('\t\t\t- Zotero link: ')
        Zotero.write('[Zotero Link](' + itemLink + ')\n')
     
        // url with citation
        Zotero.write('\t\t\t- URL: [')
        Zotero.write(creatorsS)
        Zotero.write(' (' + dateS + '). ')
        Zotero.write(titleS + '. ')
        Zotero.write(item.publicationTitle + '](' + item.url + ')\n')
        
        // abstract
        Zotero.write('\t\t- Content\n')
        Zotero.write('\t\t\t- Abstract\n')
        Zotero.write('\t\t\t\t- ' + item.abstractNote + '\n')
      }
    }
    