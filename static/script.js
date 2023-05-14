class TagInput {
  constructor() {
    this.$tagInputCol = $("#form-col");
    this.makeInput();
    this.$tagForm = $("#tag-form");
    this.$tagInput = $("#tag-input");

    this.$tagForm.on("submit", this.handleSubmit.bind(this));
  }
  handleSubmit(evt) {
    evt.preventDefault();
    const tagName = this.$tagInput.val().toLowerCase().split(" ").join("");
    console.log(tagName);
    if (!this.checkTagExists(tagName)) {
      new Tag(tagName);
    } else {
      $(`#tag_${tagName}`).prop("checked", true);
    }
    this.$tagInput.val("");
  }

  checkTagExists(tagName) {
    if ($(`#tag_${tagName}`).length) {
      return true;
    }
    return false;
  }

  makeInput() {
    const $tagForm = $("<form>").attr("id", "tag-form");
    const $tagInputDiv = $("<div>").attr("class", "form-floating");
    const $newTagInput = $("<input>").attr({
      id: "tag-input",
      type: "text",
      name: "tag",
      class: "form-control",
      placeholder: "Tag name",
    });
    const $tagLabel = $("<label>").attr("for", "tag").text("Enter a tag");

    this.$tagInputCol.append(
      $tagForm.append($tagInputDiv.append($newTagInput, $tagLabel))
    );
  }
}
class Tag {
  constructor(tagName) {
    this.tagName = tagName;
    this.$tagsRow = $("#tags-row");
    this.tagId = "";
    this.initTag();
  }
  async initTag() {
    await this.postTag();

    this.createTagPill();
  }

  createTagPill() {
    const $newCol = $("<div>").attr({ class: "col mb-1 py-o pe-1 ps-0" });
    const $newTagBtn = $("<input>").attr({
      form: "post-form",
      value: `${this.tagName}`,
      type: "checkbox",
      class: "btn-check",
      id: `tag_${this.tagName}`,
      autocomplete: "off",
      name: "tags",
      checked: true,
    });
    const $newTagLbl = $("<label>")
      .attr({
        for: `tag_${this.tagName}`,
        class:
          "btn pt-0 pb-0 pr-1 pl-1 btn-sm rounded-pill btn-outline-primary",
      })
      .text(`${this.tagName}`);
    $newCol.append($newTagBtn, $newTagLbl);
    this.$tagsRow.append($newCol);
  }

  async postTag() {
    const postTag = await axios.post("/add-tag", { tag_name: this.tagName });
  }
}

if ($("#form-col").length) {
  new TagInput();
}
