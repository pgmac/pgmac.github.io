# frozen_string_literal: true

require 'jekyll'

module Jekyll
  class TagArchivePage < Page
    def initialize(site, dir, tag, posts, paginator)
      @site    = site
      @base    = site.source
      @dir     = dir
      @name    = 'index.html'
      @path    = File.join(dir, 'index.html')
      @content = ''

      self.process(@name)

      self.data = {
        'layout'    => 'tag_page',
        'title'     => tag,
        'tag'       => tag,
        'posts'     => posts,
        'paginator' => paginator,
      }
    end
  end

  class TagPageGenerator < Generator
    safe true
    priority :low

    PER_PAGE = 10

    def generate(site)
      tag_dir = site.config['tag_page_dir'] || 'tag'

      site.tags.each do |tag, tag_posts|
        sorted      = tag_posts.sort_by(&:date).reverse
        total       = sorted.size
        total_pages = [(total.to_f / PER_PAGE).ceil, 1].max
        tag_slug    = Utils.slugify(tag)

        sorted.each_slice(PER_PAGE).with_index(1) do |page_posts, page_num|
          dir      = page_num == 1 ? "#{tag_dir}/#{tag_slug}" : "#{tag_dir}/#{tag_slug}/page/#{page_num}"
          prev_num = page_num > 1 ? page_num - 1 : nil
          next_num = page_num < total_pages ? page_num + 1 : nil

          paginator = {
            'page'               => page_num,
            'per_page'           => PER_PAGE,
            'posts'              => page_posts,
            'total_posts'        => total,
            'total_pages'        => total_pages,
            'previous_page'      => prev_num,
            'previous_page_path' => prev_num && (prev_num == 1 ? "/#{tag_dir}/#{tag_slug}/" : "/#{tag_dir}/#{tag_slug}/page/#{prev_num}/"),
            'next_page'          => next_num,
            'next_page_path'     => next_num && "/#{tag_dir}/#{tag_slug}/page/#{next_num}/",
          }

          site.pages << TagArchivePage.new(site, dir, tag, page_posts, paginator)
        end
      end
    end
  end
end
