# frozen_string_literal: true

require 'jekyll'
require 'date'

module Jekyll
  class DateArchivePage < Page
    def initialize(site, dir, title, posts)
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
        'posts'       => posts.sort_by(&:date).reverse,
        'total_posts' => posts.size,
      }
    end
  end

  class DateArchiveGenerator < Generator
    safe true
    priority :low

    BASE_PATH = 'last-week'

    def generate(site)
      posts = site.categories['Last-Week']
      return if posts.nil? || posts.empty?

      posts.group_by { |p| p.date.year }.each do |year, year_posts|
        add_page(site, "#{BASE_PATH}/#{year}", year.to_s, year_posts)

        year_posts.group_by { |p| p.date.month }.each do |month, month_posts|
          mm    = format('%02d', month)
          label = "#{Date::MONTHNAMES[month]} #{year}"
          add_page(site, "#{BASE_PATH}/#{year}/#{mm}", label, month_posts)

          month_posts.group_by { |p| p.date.day }.each do |day, day_posts|
            dd    = format('%02d', day)
            label = "#{day} #{Date::MONTHNAMES[month]} #{year}"
            add_page(site, "#{BASE_PATH}/#{year}/#{mm}/#{dd}", label, day_posts)
          end
        end
      end
    end

    private

    def add_page(site, dir, title, posts)
      site.pages << DateArchivePage.new(site, dir, title, posts)
    end
  end
end
