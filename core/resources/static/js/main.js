$(function(){

// list access
function List(selector) {
    this.root = selector;
}

List.prototype = {
    getList:function() {
      var list = [];
      console.log("getting list");
      console.log(this.test);
      this.root.children().each(function(i) {
        list.push($(this).find("a").text());
      });
      return list;
    },
    append:function(thing) {
      this.root.append(thing)
    },
    clear:function() {
      this.root.children().each(function(i) {
        this.remove()
      });
    }
};

function BList(selector) {
  this.root = selector;
}
BList.prototype = {
    getPath:function() {
      var list = [];
      this.root.children().each(function(i) {
        list.push($(this).find("a").text());
        console.log(this);
        if ($(this).hasClass("active")) {
          return false;
        }
      });
      return list;
    },
    append:function(thing) {
      // trim off anything above our current location
      console.log(this.root.children().get());
      children = this.root.children().get().reverse();
      for (i in children) {
        console.log(children[i]);
        if ($(children[i]).hasClass("active")) {
            $(children[i]).removeClass("active");
            break;
          }
        $(children[i]).remove();
      }
      // and add
      this.root.append(thing.addClass("active"));
      // breadcrumb callback
      $(thing.find("a")[0]).on("click", function(event) {
        event.preventDefault();
        $(this).parent().siblings().each(function(i) {
          console.log(this);
          $(this).removeClass('active');
        });
        $(this).parent().addClass("active");
        console.log($(this).text());
        breadcrumbs.update();
      });
      // path update complete, update file view
      this.update();
    },
    clear:function() {
      this.root.children().each(function(i) {
        this.remove();
      });
    },
    update:function() {
      list = this.getPath();
      path = "";
      for (i in list) {
        path = path + list[i] + "/";
      }
      console.log(path);
      $.post("api", {"point": "files", "what":"listing", "path":path}, showListing);
    }
};

// table access
function Table(selector) {
  this.root = selector;
}
Table.prototype = {
  clear:function() {
    this.root.children().each(function(i) {
      this.remove()
    });
  },
  addFoldersFiles:function(data) {
    // add folders
    for (i in data[0]) {
      this.root.append($("<tr>").append(          //<tr>
        $("<td>").append(
            $("<img>").attr("src", "img/folder.svg").addClass("icon-folder")).append(
            data[0][i][0])).append(    //  <td>Name</td>
        $("<td>").text(FormatDate(data[1][i][1]))).append(  //  <td>Date</td>
        $("<td>").text("---")).addClass("files-folder"));              //  <td>Size</td>
    }                                             //</tr>
    // add files
    for (i in data[1]) {
      this.root.append($("<tr>").append(          //<tr>
        $("<td>").text(data[1][i][0])).append(    //  <td>Name</td>
          $("<td>").text(FormatDate(data[1][i][1]))).append(  //  <td>Date</td>
            $("<td>").text(data[1][i][2])));      //  <td>Size</td>
    }
    // callback for folders
    $(".files-table .files-folder").on("click", function(event) {
      event.preventDefault();
      breadcrumbs.append(
        TextToCrumb(
          $($(this).find("td")[0]).text()));
    });                                             //</tr>
  }
}


function showListing(data, status) {
  // clear current file list
  filetable.clear();
  filetable.addFoldersFiles(data);


}

function TextToShare(text) {
    return $("<li>").addClass("nav-item").append(
      $("<a>").addClass("nav-link").attr("href", "#").append(
        text
      )
    );
}

function TextToCrumb(text) {
    return $("<li>").addClass("breadcrumb-item").append(
      $("<a>").attr("href", "#").append(
        text
      )
    );
}

function shareSetup(data, status) {
  for (i in data) {
    shares.append(TextToShare(data[i]));
  }

  // Share click
  $("ul.files-shares a.nav-link").on("click", function(event) {
    event.preventDefault();

    $(this).parent().siblings().each(function(i) {
      $(this).removeClass("active");
    });
    $(this).parent().addClass("active");

    $(".files-path").removeClass("files-path-hide");
    breadcrumbs.clear();
    breadcrumbs.append(TextToCrumb(this.text));
  });
}

function FormatDate(seconds) {
  d = new Date(seconds * 1000);
  dstr = d.toLocaleString();
  console.log(dstr);
  date = dstr.slice(0, dstr.indexOf(",")) +
          dstr.slice(dstr.indexOf(",") + 1,  dstr.lastIndexOf(":")) +
          " " + dstr.slice(-2);
  return date;
}

  //Download shares list and setup
  shares = new List($(".files-shares"));
  $.post("api", {"point": "files", "what":"shares"}, shareSetup);
  breadcrumbs = new BList($(".files-path"));
  filetable = new Table($(".files-table table tbody"));



});
