## app.R ##
library(shinydashboard)
library(datasets)
library(DT)
library(ggplot2)
library(plotly)

ui <- dashboardPage(
  dashboardHeader(title = "Basic dashboard"),
  dashboardSidebar(),
  dashboardBody(
    # Boxes need to be put in a row (or column)
    fluidRow(
      selectInput(inputId="species", label="Species", choices = levels(iris$Species),
                  selected=levels(iris$Species), multiple = TRUE),
      # actionButton("go", "Go"),
      DT::dataTableOutput("mytable"), # https://shiny.rstudio.com/articles/datatables.html
      # plotOutput("plot1", width=1000),
      plotlyOutput("plot2", width=1000)
    )
  )
)

server <- function(input, output) {
  
  # user_iris <- eventReactive(input$go,{
  #   iris %>% 
  #     filter(Species %in% input$species)
  # })
  
  user_iris <- reactive({
    iris %>%
      filter(Species %in% input$species)
  })

  # output$plot1 <- renderPlot({
  #   ## Can use any plot (html) package in R (native plot, ggplot)
  #   ## https://beta.rstudioconnect.com/content/2792/Interactive%20Dashboards%20Shiny.nb.html
  #   # plot(x=user_iris()$Sepal.Length, y=user_iris()$Sepal.Width, 
  #   #      xlab="Sepal Length", ylab="Sepal Width",  main="Sepal Length-Width")
  #   ggplot(data=user_iris(), aes(x = Sepal.Length, y = Sepal.Width)) +
  #     geom_point(aes(color=Species, shape=Species)) +
  #     xlab("Sepal Length") +  ylab("Sepal Width") +
  #     ggtitle("Sepal Length-Width")
  # })
  
   ## Can use any plotly, etc.
  output$plot2 <- renderPlotly({
    p<-plot_ly(data = user_iris(), x = ~Sepal.Length, 
               y = ~Petal.Length, type = "scatter", mode="markers", color=~Species)
  })
  
  output$mytable <-DT::renderDataTable({
    user_iris()
    })
}

shinyApp(ui, server)