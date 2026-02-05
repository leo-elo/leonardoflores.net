module Jekyll
  class CategoryPageGenerator < Generator
    safe true

    CATEGORIES = {
      "news" => "News",
      "presentations" => "Presentations",
      "creative-work" => "Creative Work",
      "teaching" => "Teaching",
      "resources" => "Resources",
      "en-espanol" => "En Español"
    }

    def generate(site)
      CATEGORIES.each do |slug, display_name|
        # Collect posts for this category
        posts = site.posts.docs.select do |post|
          post.data["categories"].any? { |c| c.downcase.gsub(' ', '-') == slug }
        end.sort_by { |p| p.date }.reverse

        site.pages << CategoryPage.new(site, slug, display_name, posts)
      end
    end
  end

  class CategoryPage < Page
    def initialize(site, slug, display_name, posts)
      @site = site
      @base = site.source
      @dir = "category"
      @name = "#{slug}.html"

      self.process(@name)
      self.read_yaml(File.join(@base, "_layouts"), "category.html")
      self.data["title"] = "#{display_name} - Leonardo Flores"
      self.data["category_name"] = display_name
      self.data["category_slug"] = slug
      self.data["posts"] = posts
      self.data["layout"] = "category"
    end
  end
end
