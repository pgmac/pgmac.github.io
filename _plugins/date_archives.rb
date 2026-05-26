# frozen_string_literal: true

require 'jekyll'
require 'date'

module Jekyll
  class DateArchivePage < Page
    def initialize(site, dir, title, posts, paginator)
      @site    = site
      @base    = site.source
      @dir     = dir
      @name    = 'index.html'
      @path    = File.join(dir, 'index.html')
      @content = ''

      self.process(@name)

      self.data = {
        'layout'      => 'date_archive',
        'title'       => title,
        'posts'       => posts,
        'total_posts' => paginator['total_posts'],
        'paginator'   => paginator,
      }
    end
  end

  class DateArchiveGenerator < Generator
    safe true
    priority :low

    BASE_PATH = 'last-week'
    PER_PAGE  = 10

    def generate(site)
      posts = site.categories['Last-Week']
      return if posts.nil? || posts.empty?

      posts.group_by { |p| p.date.year }.each do |year, year_posts|
        add_pages(site, "#{BASE_PATH}/#{year}", year.to_s, year_posts)

        year_posts.group_by { |p| p.date.month }.each do |month, month_posts|
          mm    = format('%02d', month)
          label = "#{Date::MONTHNAMES[month]} #{year}"
          add_pages(site, "#{BASE_PATH}/#{year}/#{mm}", label, month_posts)

          month_posts.group_by { |p| p.date.day }.each do |day, day_posts|
            dd    = format('%02d', day)
            label = "#{day} #{Date::MONTHNAMES[month]} #{year}"
            add_pages(site, "#{BASE_PATH}/#{year}/#{mm}/#{dd}", label, day_posts)
          end
        end
      end
    end

    private

    def add_pages(site, base_dir, title, posts)
      sorted      = posts.sort_by(&:date).reverse
      total       = sorted.size
      total_pages = [(total.to_f / PER_PAGE).ceil, 1].max

      sorted.each_slice(PER_PAGE).with_index(1) do |page_posts, page_num|
        dir      = page_num == 1 ? base_dir : "#{base_dir}/page/#{page_num}"
        prev_num = page_num > 1 ? page_num - 1 : nil
        next_num = page_num < total_pages ? page_num + 1 : nil

        paginator = {
          'page'               => page_num,
          'per_page'           => PER_PAGE,
          'posts'              => page_posts,
          'total_posts'        => total,
          'total_pages'        => total_pages,
          'previous_page'      => prev_num,
          'previous_page_path' => prev_num && (prev_num == 1 ? "/#{base_dir}/" : "/#{base_dir}/page/#{prev_num}/"),
          'next_page'          => next_num,
          'next_page_path'     => next_num && "/#{base_dir}/page/#{next_num}/",
        }

        site.pages << DateArchivePage.new(site, dir, title, page_posts, paginator)
      end
    end
  end
end
